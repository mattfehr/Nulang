#include <stdio.h>
#include <stdlib.h>

void swap(int arr[], int i, int j) {
    int temp = arr[i];
    arr[i] = arr[j];
    arr[j] = temp;
}

int partition(int arr[], int left, int right) {
    int pivot = arr[left];
    int i = left;
    int j = right;

    while (i < j) {
        while (i <= right && arr[i] <= pivot) {
            i++;
        }
        while (j >= left && arr[j] > pivot) {
            j--;
        }
        if (i < j) {
            swap(arr, i, j);
        }
    }
    printf("%d \n", i);
    printf("%d \n", j);
    printf("%d \n", pivot);
    swap(arr, left, j);
    return j;
}

void quick_sort(int arr[], int left, int right) {
    if (right - left < 1) return;

    int pivot_index = partition(arr, left, right);
    quick_sort(arr, left, pivot_index - 1);
    quick_sort(arr, pivot_index + 1, right);
}

int main() {
    int arr[] = {7, 2, 9, 4, 1, 8};
    int n = sizeof(arr) / sizeof(arr[0]);
    quick_sort(arr, 0, n - 1);
    for(int i = 0; i < 6; ++i) { printf("%d ", arr[i]); }
    printf("\n");
}
