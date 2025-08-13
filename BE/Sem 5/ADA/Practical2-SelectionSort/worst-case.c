#include <stdio.h>
#include <stdbool.h>
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

    bool flag;
    for (int i = 0; i < n - 1; i++)
    {
        outer_iterations++;
        flag = false;
        for (int j = 0; j < n - i - 1; j++)
        {
            inner_iterations++;
            if (arr[j] > arr[j + 1])
            {
                flag = true;
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
        if (!flag)
        {
            break;
        }
    }

    clock_t end = clock();
    double time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;

    printf("Bubble Sort (Worst Case)\n");
    printf("Time taken: %f seconds\n", time_taken);
    printf("Outer loop iterations: %d\n", outer_iterations);
    printf("Inner loop iterations: %d\n", inner_iterations);
    return 0;
}