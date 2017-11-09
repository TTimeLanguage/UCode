#include <stdio.h>

int a(int b, int c) {
	return b*c;
}

int main() {
	int b = 3, c = 5;
	printf("%d ", b);
	c = b*a(b, c);
	printf("%d ", c);
}
