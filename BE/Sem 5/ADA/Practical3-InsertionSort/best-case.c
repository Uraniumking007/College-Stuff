#include <stdio.h>
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

    for (int i = 1; i < n; i++)
    {
        int key = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > key)
        {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = key;
    }

    clock_t end = clock();
    double time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;

    printf("Insertion Sort (Best Case)\n");
    printf("Time taken: %f seconds\n", time_taken);

    return 0;
}
