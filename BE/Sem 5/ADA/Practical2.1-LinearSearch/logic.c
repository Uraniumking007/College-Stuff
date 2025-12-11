#include <stdio.h>
#include <time.h>

#define MAX_SIZE 10000

typedef struct
{
    int index;
    int comparisons;
} LinearSearchResult;

LinearSearchResult linear_search(const int array[], int length, int key)
{
    LinearSearchResult result = {.index = -1, .comparisons = 0};

    for (int i = 0; i < length; i++)
    {
        result.comparisons++;
        if (array[i] == key)
        {
            result.index = i;
            break;
        }
    }

    return result;
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

    if (n > MAX_SIZE)
    {
        printf("Array size exceeds maximum supported (%d).\n", MAX_SIZE);
        return 1;
    }

    int array[MAX_SIZE];

    printf("Enter %d elements:\n", n);
    for (int i = 0; i < n; i++)
    {
        if (scanf("%d", &array[i]) != 1)
        {
            printf("Invalid input.\n");
            return 1;
        }
    }

    int key;
    printf("Enter the key to search: ");
    if (scanf("%d", &key) != 1)
    {
        printf("Invalid key.\n");
        return 1;
    }

    clock_t start_time = clock();
    LinearSearchResult search_result = linear_search(array, n, key);
    clock_t end_time = clock();

    double elapsed_seconds = (double)(end_time - start_time) / CLOCKS_PER_SEC;

    if (search_result.index >= 0)
    {
        printf("Key found at index %d.\n", search_result.index);
    }
    else
    {
        printf("Key not found.\n");
    }

    printf("Comparisons: %d\n", search_result.comparisons);
    printf("Time taken: %.9f seconds\n", elapsed_seconds);
    return 0;
}


