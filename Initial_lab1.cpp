#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include <string>
#include <vector>
#include <cmath>

const float G = 9.8f;

void log(float timeInMaxPoint, float height) {
	printf("t=%f, s=%f\n", timeInMaxPoint, height);
}

float calcCurHeight(float timeInMaxPoint, float curTime) {
	float speedInMaxPoint = G * timeInMaxPoint;

	return speedInMaxPoint * curTime - 0.5 * G * curTime * curTime;
}

int main(int, char *[])
{
	float timeInMaxPoint,
		  speedInMaxPoint,
		  heightInTheEnd,
		  timeInTheEnd,
		  height;
	bool flag = false;

	printf("Height in max point: ");
	if (0 == scanf("%d", &height))
	{
		printf("\n" "expected floating-point number" "\n");
		exit(1);
	}

	timeInMaxPoint = sqrt(height * 2 / G);
	printf("T=%f\n", timeInMaxPoint);

	for (float curTime = 0; curTime < timeInMaxPoint * 2; curTime += 0.1f) {
		//an additional step to calc and log the special point
		if (curTime > timeInMaxPoint && !flag)
		{
			flag = true;
			log(timeInMaxPoint, calcCurHeight(timeInMaxPoint, timeInMaxPoint));
		}

		//a common step
		log(curTime, calcCurHeight(timeInMaxPoint, curTime));
	}

	speedInMaxPoint = G * timeInMaxPoint;
	heightInTheEnd = speedInMaxPoint * (timeInMaxPoint*2) - 0.5 * G * (timeInMaxPoint*2) * (timeInMaxPoint*2);
	timeInTheEnd = timeInMaxPoint * 2;

	log( timeInTheEnd, heightInTheEnd );

	puts("Press any key to continue...");
	system("pause");

	return 0;
}