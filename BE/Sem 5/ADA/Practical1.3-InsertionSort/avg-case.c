#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main()
{
    int n = 10000;
    int arr[10000];
    int inner_iterations = 0;
    int outer_iterations = 0;

    // Seed random number generator
    srand((unsigned int)time(NULL));

    // Fill array with random values (average case for insertion sort)
    for (int i = 0; i < n; i++)
    {
        arr[i] = rand();
    }

    clock_t start = clock();

    // Insertion sort
    for (int i = 1; i < n; i++)
    {
        outer_iterations++;
        int key = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > key)
        {
            arr[j + 1] = arr[j];
            inner_iterations++;
            j--;
        }
        arr[j + 1] = key;
    }

    clock_t end = clock();
    double time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;

    printf("Insertion Sort (Average Case)\n");
    printf("Time taken: %f seconds\n", time_taken);
    printf("Outer loop iterations: %d\n", outer_iterations);
    printf("Inner loop iterations: %d\n", inner_iterations);

    return 0;
}
