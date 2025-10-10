#include <stdio.h>
#include <stdlib.h>
#include <time.h>

static void swap(int *a, int *b) { int t = *a; *a = *b; *b = t; }

static int partition(int *array, int low, int high)
{
    int pivot = array[high];
    int i = low - 1;
    for (int j = low; j <= high - 1; j++)
    {
        if (array[j] <= pivot)
        {
            i++;
            swap(&array[i], &array[j]);
        }
    }
    swap(&array[i + 1], &array[high]);
    return i + 1;
}

static void quick_sort(int *array, int low, int high)
{
    if (low < high)
    {
        int pi = partition(array, low, high);
        quick_sort(array, low, pi - 1);
        quick_sort(array, pi + 1, high);
    }
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

    // Best case: already random with good pivots; use shuffled data
    srand((unsigned)time(NULL));
    for (int i = 0; i < n; i++) array[i] = rand();

    clock_t start_time = clock();
    quick_sort(array, 0, n - 1);
    clock_t end_time = clock();

    double elapsed_seconds = (double)(end_time - start_time) / CLOCKS_PER_SEC;

    printf("Time taken (best/average-like random input): %.9f seconds\n", elapsed_seconds);

    free(array);
    return 0;
}


