#include <stdio.h>
#include <stdbool.h>

int main()
{
    int arr[] = {1, 2, 3, 4};
    int n = sizeof(arr) / sizeof(arr[0]); // Calculate number of elements
    bool flag = false;

    // Bubble sort implementation
    for (int i = 0; i < n - 1; i++)
    {
        flag = false;                       // Reset flag for each pass
        for (int j = 0; j < n - i - 1; j++) // Fixed: increment j, correct condition
        {
            if (arr[j] > arr[j + 1]) // Compare adjacent elements
            {
                flag = true;
                // Swap elements
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
        // If no swaps occurred, array is sorted
        if (!flag)
        {
            break;
        }
    }

    // Print the sorted array
    for (int i = 0; i < n; i++)
    {
        printf("%d ", arr[i]);
    }
    printf("\n");

    return 0;
}