#include <stdio.h>

int foo(int n) {
	if (n < 3) return 1;
	return foo(n - 1) + foo(n - 2);
}

int main() {
	int n, re;

	scanf("%d", &n);

	re = foo(n);
	printf("%d", re);
}