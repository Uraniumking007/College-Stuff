#include <stdio.h>
#include <stdbool.h>
#include <time.h>

int main()
{
    int n = 10000;
    int arr[10000];

    for (int i = 0; i < n; i++)
    {
        arr[i] = i + 1;
    }

    clock_t start = clock();

    bool flag;
    for (int i = 0; i < n - 1; i++)
    {
        flag = false;
        for (int j = 0; j < n - i - 1; j++)
        {
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

    printf("Bubble Sort (Best Case)\n");
    printf("Time taken: %f seconds\n", time_taken);

    return 0;
}