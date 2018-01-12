#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include <string>
#include <vector>
#include <cmath>

int main(int, char *[])
{
	const float g = 9.8f;
	float T, Vn;
	int S, M;
	printf("S: ");
	if (0 == scanf("%d", &S))
	{
		printf("\n" "expected floating-point number" "\n");
		exit(1);
	}

	// T - time point when height is at maximum.
	// t - current time point
	// v(0) = g * T
	// v(t) == v(0) - g * t
	// s(t) == v(0) * t - 0.5 * g * t * t
	T = sqrt(S * 2 / g);
	printf("T=%f\n", T);
	bool flag = false;
	for (float t=0; t<T*2;t+=0.1f) {
		if (t>T&&!flag)
		{
			flag=true;
			float V0=  g*T;
			float s = V0 * T - 0.5 * g * T * T;
			printf("t=%f, s=%f\n", T, s);
		}
		float V0 = g * T;
		float s =V0*t -0.5 *g*t*t;
		printf( "t=%f, s=%f\n", t, s );
	}



	float V0 = g*T, s = V0*(T*2) - 0.5*g*(T*2)*(T*2);
	printf("t=%f, s=%f\n", T*2,s);

	// Pause program until any key pressed.
	puts("Press any key to continue...");
	system("pause");

	return 0;
}
