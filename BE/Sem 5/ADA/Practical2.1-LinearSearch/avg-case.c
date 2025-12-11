#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int linear_search(const int *array, int length, int key, int *out_comparisons)
{
    int comparisons = 0;
    for (int i = 0; i < length; i++)
    {
        comparisons++;
        if (array[i] == key)
        {
            if (out_comparisons)
            {
                *out_comparisons = comparisons;
            }
            return i;
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

    // Initialize array with ascending values
    for (int i = 0; i < n; i++)
    {
        array[i] = i + 1;
    }

    // Average case: key roughly in the middle
    int mid_index = n / 2;
    if (mid_index >= n)
    {
        mid_index = n - 1;
    }
    int key = array[mid_index];

    int comparisons = 0;
    clock_t start_time = clock();
    int index = linear_search(array, n, key, &comparisons);
    clock_t end_time = clock();

    double elapsed_seconds = (double)(end_time - start_time) / CLOCKS_PER_SEC;

    printf("Average-case: key = %d\n", key);
    printf("Index: %d\n", index);
    printf("Comparisons: %d\n", comparisons);
    printf("Time taken: %.9f seconds\n", elapsed_seconds);

    free(array);
    return 0;
}


