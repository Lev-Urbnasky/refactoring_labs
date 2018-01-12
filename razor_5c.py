"""
Simple script to process .csv report file as per RT:469607
(see ArgumentParser description below).
"""

__version__ = '0.2.1'
__author__ = 'Alexey Demidyuk <ademidyuk@iponweb.net> & Lev Urbansky <lurbansky@iponweb.net>'

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
    totals_by_publisher = defaultdict(lambda: {'invalid_imps': 0, 'invalid_imps_cost': 0})

    logging.info('Reading "{}"'.format(report_filename))

    first_row = True

    # Read report file. Expected format:
    # Publisher ID,Invalid Impressions,Invalid Impression Cost (USD)
    # adconductor_1000764754,1,0.01
    # ...
    with open(report_filename) as f:
        reader = csv.DictReader(
            f, ['pub_id','imps','cost', 'invalid_imps', 'invalid_imps_cost']
        )

        # Skip 1st line with header
        next(reader)

        for line in reader:
            publisher = extract_publisher(line['pub_id'])

            # Save original values
            data_by_publisher[publisher].append((
                line['pub_id'],
                line['imps'],
                line['cost'],
                line['invalid_imps'],
                line['invalid_imps_cost']
            ))

            # Calculate totals
            totals_by_publisher[publisher]['invalid_imps'] += int(
                line['invalid_imps']
            )
            totals_by_publisher[publisher]['invalid_imps_cost'] += float(
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
        if is_ssps_over_limit(args.spend_limiter_USD,totals_by_publisher[publisher]['invalid_imps_cost'],publisher) == True:
            subfolder = generate_subfolder(generate_output_foldername(report_filename),args.spend_limiter_USD)
            publisher_fname = os.path.join(
                subfolder,
                generate_ssp_filename(report_filename, publisher)
            )
        else:
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
                publisher_totals['invalid_imps'],
                round(publisher_totals['invalid_imps_cost'], 2),
            ])
            writer.writerow([])

            writer.writerow([
                'Publisher ID',
                'Invalid Impressions',
                'Invalid Impression Cost (USD)',
            ])

            for pub_id, imps, cost, invalid_imps, invalid_imps_cost in data:
                writer.writerow([pub_id, invalid_imps, invalid_imps_cost])

            sum_table = generate_sum_table(output_folder, report_filename)

            first_row = add_to_sum(sum_table, totals_by_publisher, publisher, first_row)
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


def is_ssps_over_limit(spend_limiter_USD: float, spend: float, ssp_name: str
                       ) -> bool:
    """
    It is needed to find SSPs which spends are more then limit
    and copy their reports to the subfolder
    <report filename without extension>/spent_more_then_<args.spend_limiter_USD>_USD

    E.g.:

    find_ssps_over_limit(100.0, 200.0, adconductor
    ) -> true
    """
    if spend >= spend_limiter_USD:
        return True
    return False


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


def generate_output_foldername(report_filename: str) -> str:
    """
    Take source report filename and generate
    following foldername for output folder:
    <report filename without extension>

    E.g.:

    generate_output_folder with such name(
        "src/dbm_BidSwitch_ivt_by_pub_id_2017-10-09_to_2017-10-15.csv")
        -> "dbm_BidSwitch_ivt_by_pub_id_2017-10-09_to_2017-10-15"
    """
    #inPath=os.path.abspath(report_filename)
    return '{}'.format(
        os.path.splitext(os.path.basename(report_filename))[0]
        )

def generate_sum_table(output_folder: str, report_filename: str) -> str:
    """
        Take source report filename and generate
        filename for SUM report:
        SUM_<report filename without extension>.csv

        E.g.:

        generate_sum_table with such name(
            "src/dbm_BidSwitch_ivt_by_pub_id_2017-10-09_to_2017-10-15.csv")
            -> "SUM_dbm_BidSwitch_ivt_by_pub_id_2017-10-09_to_2017-10-15.csv"
        """
    return '{0}/SUM_{1}.csv'.format(
        output_folder,
        os.path.splitext(os.path.basename(report_filename))[0]
    )

def add_to_sum(sum_table: str, totals_by_publisher, publisher, first_row) -> bool:
    """
            Take SUM Table name, Total Invalid Values,
            Publisher(SSP) name, First Row Flag
            and appends First Row line if Flag is True
            appends Values if False
            then returns False

            E.g.:

            add_to_sum(SUM_dbm_BidSwitch_ivt_by_pub_id_2017-10-09_to_2017-10-15.csv, totals_by_publisher[adconductor], adconductor, True)
                SSP Name -> Total Invalids -> Total_Invalids_Cost
            """
    with open(sum_table, 'a') as f:
        writer = csv.writer(f)

        if first_row == True:
            writer.writerow([
                'SSP Name',
                'Total Invalid Impressions',
                'Total Invalid Impression Cost (USD)',
            ])

        publisher_totals = totals_by_publisher[publisher]
        writer.writerow([
            publisher,
            publisher_totals['invalid_imps'],
            round(publisher_totals['invalid_imps_cost'], 2),
        ])
    return False

def generate_subfolder(output_foldername: str,spend_limiter_USD: float) -> str:
    """
    Take source report filename and generate
    following foldername for output subfolder:
    spent_more_then_<spend_limiter_USD>_USD

    E.g.:

    generate_sublolder(100.0)
        -> "dbm_BidSwitch_ivt_by_pub_id_2017-10-09_to_2017-10-15/spent_more_then_100.0_USD"
    """
    subfolder_name = "{0}/spent_more_then_{1}_USD".format(output_foldername, spend_limiter_USD)
    if not os.path.isdir(subfolder_name):
        os.mkdir(subfolder_name)
    return subfolder_name

if __name__ == '__main__':
    """Entry-point"""

    parser = argparse.ArgumentParser(
        description='Takes .csv file with fraud info, groups lines by ssp, '
                    'creates .csv file for each ssp with specified filename,'
                    'each file contains invalid imp values and totals.'
                    'Reports, that contains more then spend_limiter_USD spend'
                    'stores in specific folder.'
                    'SUM Table contains all of the total values grouped by SSP.'
    )
    parser.add_argument(
        'report_file',
        type=str,
        help='Path to source .csv file with fraud info'
    )
    parser.add_argument(
        'spend_limiter_USD',
        type=float,
        help='Spend limit SSPs above which must stay in separate folder'
        )

    args = parser.parse_args()

    if not os.path.isfile(args.report_file):
        print('Specified report file "{}" doesn\'t exist'.format(
            args.report_file
        ))
        exit(2)

    output_foldername = generate_output_foldername(args.report_file)

    if not os.path.isdir(output_foldername):
        print('Specified output folder "{}" doesn\'t exist. Will be created'.format(
            output_foldername
        ))
        os.mkdir(output_foldername)

    if not os.path.isdir(output_foldername):
        print('Someting went wrong and specified output folder "{}" still doesn\'t exist.'.format(
            output_foldername
        ))
        exit(3)

    process(args.report_file, output_foldername)