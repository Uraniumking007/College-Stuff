#include <stdio.h>
#include <stdlib.h>
#include <time.h>

static void swap(int *a, int *b) { int t = *a; *a = *b; *b = t; }

static void heapify(int *array, int n, int i)
{
    int largest = i;
    int left = 2 * i + 1;
    int right = 2 * i + 2;

    if (left < n && array[left] > array[largest]) largest = left;
    if (right < n && array[right] > array[largest]) largest = right;

    if (largest != i)
    {
        swap(&array[i], &array[largest]);
        heapify(array, n, largest);
    }
}

static void heap_sort(int *array, int n)
{
    for (int i = n / 2 - 1; i >= 0; i--) heapify(array, n, i);
    for (int i = n - 1; i >= 0; i--)
    {
        swap(&array[0], &array[i]);
        heapify(array, i, 0);
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

    printf("Enter %d elements:\n", n);
    for (int i = 0; i < n; i++)
    {
        if (scanf("%d", &array[i]) != 1)
        {
            printf("Invalid input.\n");
            free(array);
            return 1;
        }
    }

    clock_t start_time = clock();
    heap_sort(array, n);
    clock_t end_time = clock();

    double elapsed_seconds = (double)(end_time - start_time) / CLOCKS_PER_SEC;

    printf("Sorted array:\n");
    for (int i = 0; i < n; i++) printf("%d ", array[i]);
    printf("\nTime taken: %.9f seconds\n", elapsed_seconds);

    free(array);
    return 0;
}


