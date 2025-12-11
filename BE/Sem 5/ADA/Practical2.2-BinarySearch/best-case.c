#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int binary_search(const int *array, int length, int key, int *out_comparisons)
{
    int left = 0;
    int right = length - 1;
    int comparisons = 0;
    while (left <= right)
    {
        int mid = left + (right - left) / 2;
        comparisons++;
        if (array[mid] == key)
        {
            if (out_comparisons)
            {
                *out_comparisons = comparisons;
            }
            return mid;
        }
        else if (array[mid] < key)
        {
            left = mid + 1;
        }
        else
        {
            right = mid - 1;
        }
    }
    if (out_comparisons)
    {
        *out_comparisons = comparisons;
    }
    return -1;
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

    for (int i = 0; i < n; i++)
    {
        array[i] = i + 1;
    }

    // Best case: key equals the middle element
    int mid = n / 2;
    int key = array[mid];

    int comparisons = 0;
    clock_t start_time = clock();
    int index = binary_search(array, n, key, &comparisons);
    clock_t end_time = clock();

    double elapsed_seconds = (double)(end_time - start_time) / CLOCKS_PER_SEC;

    printf("Best-case: key = %d\n", key);
    printf("Index: %d\n", index);
    printf("Comparisons: %d\n", comparisons);
    printf("Time taken: %.9f seconds\n", elapsed_seconds);

    free(array);
    return 0;
}


