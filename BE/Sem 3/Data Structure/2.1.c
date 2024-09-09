#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

int binary_search(int arr[], int searchTerm, int size)
{
    int low = 0, high = size - 1, mid;
    while (low <= high)
    {
        mid = (low + high) / 2;
        if (arr[mid] == searchTerm)
        {
            return mid;
        }
        else if (arr[mid] < searchTerm)
        {
            low = mid + 1;
        }
        else
        {
            high = mid - 1;
        }
    }
    return -1;
}

int main()
{
    int *arr;
    int size;
    int searchTerm;
    bool exit = false;

    printf("Enter Size of Array: ");
    scanf("%d", &size);

    arr = (int *)malloc(size * sizeof(int));

    printf("\n\nEnter Array Elements: \n");
    for (int i = 0; i < size; i++)
    {
        scanf("%d", &arr[i]);
    }

    while (!exit)
    {
        if (!exit)
        {
            printf("Enter Search Term\n");
            scanf("%d", &searchTerm);
            printf("Value %d is found at index %d ", searchTerm, binary_search(arr, searchTerm, size));
        }
    }

    free(arr);
    return 0;
}