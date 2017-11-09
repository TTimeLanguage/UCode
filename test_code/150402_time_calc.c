#include <stdio.h>

void timeCalc(int hour, int min, int minToAdd) {
	min += minToAdd;
	if (min > 60) {
		hour += min / 60;
		min %= 60;
		if (hour > 23) hour %= 24;
	}
	printf("%d %d\n", hour, min);
}

void timeCalc2(int hour, int min, int minToAdd) {
	min += hour * 60 + minToAdd;
	hour = (min / 60) % 24;
	min %= 60;
	printf("%d %d\n", hour, min);
}

int main() {
	int hour, min, minToAdd;

	scanf("%d", &hour);
	scanf("%d", &min);
	scanf("%d", &minToAdd);

	timeCalc(hour, min, minToAdd);
	timeCalc2(hour, min, minToAdd);
}