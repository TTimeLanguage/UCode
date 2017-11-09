#include <stdio.h>

int prime[1000] = { 1, 1 };

void f(int i) {
	int j = i + i;
	for (; j < 1000; j += i) {
		prime[j] = 1;
	}
}

int main() {
	int i = 2;
	for (; i <= 32; i++) {
		if (!prime[i]) f(i);
	}
	for (i = 2; i < 1000; i++) {
		if (!prime[i]) printf("%d ", i);
	}
}