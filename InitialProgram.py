"""
Simple script to process .csv report file as per RT:469607
(see ArgumentParser description below).
"""

__version__ = '0.0.3'
__author__ = 'Alexey Demidyuk <ademidyuk@iponweb.net>'

import os
import argparse
import csv
import logging
from collections import defaultdict


logging.basicConfig(
    format='%(asctime)s\t%(levelname)s\t(%(name)s)\t%(message)s',
    level=logging.INFO,
)
logger = logging.getLogger('invalid_reports')


def process(report_filename: str, output_folder: str):
    """
    Read provided `report_filename` with .csv data,
    group by ssp and write .csv file for each ssp from report
    with totals and original values (save files to `output_folder`)
    """

    # To store original values from report
    data_by_publisher = defaultdict(list)

    # To store calculated totals
    totals_by_publisher = defaultdict(lambda: {'imps': 0, 'cost': 0})

    logging.info('Reading "{}"'.format(report_filename))

    # Read report file. Expected format:
    # Publisher ID,Invalid Impressions,Invalid Impression Cost (USD)
    # adconductor_1000764754,1,0.01
    # ...
    with open(report_filename) as f:
        reader = csv.DictReader(
            f, ['pub_id', 'invalid_imps', 'invalid_imps_cost']
        )

        # Skip 1st line with header
        next(reader)

        for line in reader:
            publisher = extract_publisher(line['pub_id'])

            # Save original values
            data_by_publisher[publisher].append((
                line['pub_id'],
                line['invalid_imps'],
                line['invalid_imps_cost']
            ))

            # Calculate totals
            totals_by_publisher[publisher]['imps'] += int(
                line['invalid_imps']
            )
            totals_by_publisher[publisher]['cost'] += float(
                line['invalid_imps_cost']
            )

    # Write files for each ssp. Output format:
    # total,163437,1130.41
    #
    # Publisher ID,Invalid Impressions,Invalid Impression Cost (USD)
    # adconductor_1000764754,1,0.01
    # ...
    files_created_count = 0
    for publisher, data in data_by_publisher.items():
        publisher_fname = os.path.join(
            output_folder,
            generate_ssp_filename(report_filename, publisher)
        )

        if os.path.isfile(publisher_fname):
            logging.info('Overwriting "{}"'.format(publisher_fname))
        else:
            logging.info('Creating "{}"'.format(publisher_fname))

        with open(publisher_fname, 'w') as f:
            writer = csv.writer(f)

            publisher_totals = totals_by_publisher[publisher]
            writer.writerow([
                'total',
                publisher_totals['imps'],
                round(publisher_totals['cost'], 2),
            ])
            writer.writerow([])

            writer.writerow([
                'Publisher ID',
                'Invalid Impressions',
                'Invalid Impression Cost (USD)',
            ])

            for pub_id, imps, cost in data:
                writer.writerow([pub_id, imps,  cost])

        files_created_count += 1

    logging.info('Finished, created files: {}'.format(files_created_count))


def extract_publisher(pub_id: str) -> str:
    """
    Publisher id column from report .csv file has following format:
    "adconductor_1000764754".
    Take that string and extract ssp name. E.g.

    "adconductor_1000764754" -> "adconductor"
    "gumgum_1287181553_12980" -> "gumgum"
    """

    parts = pub_id.split('_')
    return '_'.join(parts[:1])


def generate_ssp_filename(report_filename: str, publisher: str) -> str:
    """
    Take source report filename, publisher name
    and generate following filename for ssp file:

    <report filename without extension>_<ssp>.csv

    E.g.:

    generate_ssp_filename(
        "src/dbm_BidSwitch_ivt_by_pub_id_2017-10-09_to_2017-10-15.csv",
        "adconductor"
    ) -> "adconductor_dbm_BidSwitch_ivt_by_pub_id_2017-10-09_to_2017-10-15.csv"
    """

    return '{}_{}.csv'.format(
        publisher,
        os.path.splitext(os.path.basename(report_filename))[0]
    )


if __name__ == '__main__':
    """Entry-point"""

    parser = argparse.ArgumentParser(
        description='Takes .csv file with fraud info, groups lines by ssp, '
                    'creates .csv file for each ssp '
                    'with original values and totals'
    )
    parser.add_argument(
        'report_file',
        type=str,
        help='Path to source .csv file with fraud info'
    )
    parser.add_argument(
        'output_folder',
        type=str,
        help='Output folder where .csv files per ssp will be created'
    )

    args = parser.parse_args()

    if not os.path.isfile(args.report_file):
        print('Specified report file "{}" doesn\'t exist'.format(
            args.report_file
        ))
        exit(1)

    if not os.path.isdir(args.output_folder):
        print('Specified output folder "{}" doesn\'t exist. Will be created'.format(
            args.output_folder
        ))
        os.mkdir(args.output_folder)
        if not os.path.isdir(args.output_folder):
            print('Someting went wrong and specified output folder "{}" doesn\'t exist.'.format(
                args.output_folder
            ))
            exit(1)
    process(args.report_file, args.output_folder)