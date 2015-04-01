#include <stdio.h>

void setElt(int arr[], int max) {
	int i = 0;

	for (; i < max; i++) {
		arr[i] = i;
	}
}

int getElt(int n, int arr[]) {
	return arr[n];
}

int main() {
	int arr[100], re;
	setElt(arr, 100);
	re = getElt(33, arr);
	printf("%d", re);
}