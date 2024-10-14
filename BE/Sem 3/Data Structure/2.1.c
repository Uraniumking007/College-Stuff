#include <stdio.h>

#define MAX 100

int binarySearch(int arr[], int size, int target)
{
    int left = 0;
    int right = size - 1;

    while (left <= right)
    {
        int mid = left + (right - left) / 2;

        if (arr[mid] == target)
            return mid;

        if (arr[mid] < target)
            left = mid + 1;

        else
            right = mid - 1;
    }

    return -1;
}

int main()
{
    int arr[MAX];
    int size, target;

    printf("Enter the number of elements in the array: ");
    scanf("%d", &size);

    printf("Enter %d elements: ", size);
    for (int i = 0; i < size; i++)
    {
        scanf("%d", &arr[i]);
    }

    printf("Enter the element to be searched: ");
    scanf("%d", &target);

    int result = binarySearch(arr, size, target);

    if (result != -1)
        printf("Element is present at index %d\n", result);
    else
        printf("Element is not present in array\n");

    return 0;
}