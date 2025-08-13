#include <stdio.h>
#include <stdbool.h>

int take_input(int arr[])
{
    int n;
    printf("Enter the number of elements in the array: ");
    scanf("%d", &n);
    printf("Enter the elements of the array:\n");
    for (int i = 0; i < sizeof(arr); i++)
    {
        scanf("%d", &arr[i]);
    }
    return n;
}

int print_array(int arr[])
{

    for (int i = 0; i < sizeof(arr); i++)
    {
        printf("%d ", arr[i]);
    }
}

int bubblesort(int arr[], bool flag, int outterloop, int innerloop)
{
    for (int i = 0; i < sizeof(arr) - 1; i++)
    {
        flag = false;
        for (int j = 0; j < sizeof(arr) - i - 1; j++)
        {
            printf("Iterations %d \n", outterloop);
            if (arr[j] > arr[j + 1])
            {
                flag = true;
                // Swap elements
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
                printf("Iteration %d values swapped %d and %d \n", innerloop, arr[j], arr[j + 1]);
                innerloop++;
            }
            outterloop++;
        }
        if (!flag)
        {
            break;
        }
    }
}

int main()
{
    int arr[10];

    take_input(arr);

    bool flag = false;

    int outterloop = 1;
    int innerloop = 1;

    // Print Array
    printf("Original array: ");
    print_array(arr);

    printf("\n");
    bubblesort(arr, flag, outterloop, innerloop);

    // Print the sorted array
    printf("Sorted array: ");
    print_array(arr);
    printf("\n");

    return 0;
}