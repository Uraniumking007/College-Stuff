
#include <stdio.h>
#include <time.h>

int main()
{
    int n = 10000;
    int arr[10000];
    int inner_iterations = 0;
    int outer_iterations = 0;

    for (int i = 0; i < n; i++)
    {
        arr[i] = n - i;
    }

    clock_t start = clock();

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

    printf("Insertion Sort (Worst Case)\n");
    printf("Time taken: %f seconds\n", time_taken);
    printf("Outer loop iterations: %d\n", outer_iterations);
    printf("Inner loop iterations: %d\n", inner_iterations);

    return 0;
}
