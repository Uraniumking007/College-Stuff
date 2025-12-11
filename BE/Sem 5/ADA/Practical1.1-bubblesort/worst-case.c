#include <stdio.h>
#include <stdbool.h>
#include <time.h>

int main()
{
    int arr[10000];
    int innerloop = 1;
    int outterloop = 1;
    for (int i = 0; i < 10000; i++)
    {
        arr[i] = 10000 - i;
    }
    int n = sizeof(arr) / sizeof(arr[0]);
    bool flag = false;

    clock_t start = clock();

    // Bubble sort implementation
    for (int i = 0; i < n - 1; i++)
    {
        outterloop++;
        flag = false;
        for (int j = 0; j < n - i - 1; j++)
        {
            innerloop++;
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
    printf("Outer Loop Iterations: %d \n", outterloop);
    printf("Inner Loop Iterations: %d \n", innerloop);
    printf("Time taken: %f seconds \n", time_taken);

    return 0;
}