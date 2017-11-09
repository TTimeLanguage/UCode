#include <stdio.h>

int gcd(int a, int b) {
	int tmp;
	while (b) {
		tmp = a%b;
		a = b;
		b = tmp;
	}
	return a;
}

int gcd2(int a, int b) {
	if (!b) return a;
	return gcd2(b, a%b);
}

int main() {
	int n, a, b;
	scanf("%d", &n);
	while (n--) {
		scanf("%d %d", &a, &b);
		printf("%d\n", (a*b) / gcd(a, b));
		printf("%d\n", (a*b) / gcd2(a, b));
	}
}