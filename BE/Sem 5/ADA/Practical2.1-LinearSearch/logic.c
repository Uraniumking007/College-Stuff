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

    int key;
    printf("Enter the key to search: ");
    if (scanf("%d", &key) != 1)
    {
        printf("Invalid key.\n");
        free(array);
        return 1;
    }

    int comparisons = 0;
    clock_t start_time = clock();
    int index = linear_search(array, n, key, &comparisons);
    clock_t end_time = clock();

    double elapsed_seconds = (double)(end_time - start_time) / CLOCKS_PER_SEC;

    if (index >= 0)
    {
        printf("Key found at index %d.\n", index);
    }
    else
    {
        printf("Key not found.\n");
    }

    printf("Comparisons: %d\n", comparisons);
    printf("Time taken: %.9f seconds\n", elapsed_seconds);

    free(array);
    return 0;
}


