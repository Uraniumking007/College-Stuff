#include <stdio.h>
#include <stdlib.h>
#include <time.h>

static void merge(int *array, int left, int mid, int right)
{
    int n1 = mid - left + 1;
    int n2 = right - mid;

    int *L = (int *)malloc(sizeof(int) * (size_t)n1);
    int *R = (int *)malloc(sizeof(int) * (size_t)n2);

    for (int i = 0; i < n1; i++) L[i] = array[left + i];
    for (int j = 0; j < n2; j++) R[j] = array[mid + 1 + j];

    int i = 0, j = 0, k = left;
    while (i < n1 && j < n2)
    {
        if (L[i] <= R[j]) array[k++] = L[i++];
        else array[k++] = R[j++];
    }
    while (i < n1) array[k++] = L[i++];
    while (j < n2) array[k++] = R[j++];

    free(L);
    free(R);
}

static void merge_sort(int *array, int left, int right)
{
    if (left >= right) return;
    int mid = left + (right - left) / 2;
    merge_sort(array, left, mid);
    merge_sort(array, mid + 1, right);
    merge(array, left, mid, right);
}

int main()
{
    int n;
    printf("Enter the number of elements: ");
    if (scanf("%d", &n) != 1 || n <= 0)
    {
        printf("Invalid size.\n");
        return 1;
    }

    int *array = (int *)malloc(sizeof(int) * (size_t)n);
    if (!array)
    {
        printf("Memory allocation failed.\n");
        return 1;
    }

    // Worst case for merge sort is also O(n log n); use reverse-sorted input
    for (int i = 0; i < n; i++) array[i] = n - i;

    clock_t start_time = clock();
    merge_sort(array, 0, n - 1);
    clock_t end_time = clock();

    double elapsed_seconds = (double)(end_time - start_time) / CLOCKS_PER_SEC;

    printf("Time taken (worst-case, reverse-sorted input): %.9f seconds\n", elapsed_seconds);

    free(array);
    return 0;
}


