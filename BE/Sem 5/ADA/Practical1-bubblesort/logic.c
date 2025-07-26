#include <stdio.h>
#include <stdbool.h>

int main()
{
    int arr[] = {64, 34, 25, 12, 22, 11, 90}; // Changed to unsorted array
    int n = sizeof(arr) / sizeof(arr[0]);
    bool flag = false;

    printf("Original array: ");
    for (int i = 0; i < n; i++)
    {
        printf("%d ", arr[i]);
    }
    printf("\n");

    // Bubble sort implementation
    for (int i = 0; i < n - 1; i++)
    {
        flag = false;
        for (int j = 0; j < n - i - 1; j++)
        {
            if (arr[j] > arr[j + 1])
            {
                flag = true;
                // Swap elements
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

    // Print the sorted array
    printf("Sorted array: ");
    for (int i = 0; i < n; i++)
    {
        printf("%d ", arr[i]);
    }
    printf("\n");

    return 0;
}