#include <stdio.h>
#include <stdbool.h>

#define MAX_SIZE 100

void readArray(int arr[], int *size)
{
    printf("Enter the size of the array (max %d): ", MAX_SIZE);
    scanf("%d", size);

    printf("Enter %d elements:\n", *size);
    for (int i = 0; i < *size; i++)
    {
        scanf("%d", &arr[i]);
    }
}

void displayArray(int arr[], int size)
{
    printf("Array elements: ");
    for (int i = 0; i < size; i++)
    {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

void insertElement(int arr[], int *size, int element, int index)
{
    if (*size >= MAX_SIZE)
    {
        printf("Array is full. Cannot insert.\n");
        return;
    }
    if (index < 0 || index > *size)
    {
        printf("Invalid index.\n");
        return;
    }
    for (int i = *size; i > index; i--)
    {
        arr[i] = arr[i - 1];
    }
    arr[index] = element;
    (*size)++;
}

void deleteElement(int arr[], int *size, int index)
{
    if (index < 0 || index >= *size)
    {
        printf("Invalid index.\n");
        return;
    }
    for (int i = index; i < *size - 1; i++)
    {
        arr[i] = arr[i + 1];
    }
    (*size)--;
}

void appendArray(int arr1[], int *size1, int arr2[], int size2)
{
    if (*size1 + size2 > MAX_SIZE)
    {
        printf("Not enough space to append entire array.\n");
        return;
    }
    for (int i = 0; i < size2; i++)
    {
        arr1[*size1 + i] = arr2[i];
    }
    *size1 += size2;
}

void reverseArray(int arr[], int size)
{
    for (int i = 0; i < size / 2; i++)
    {
        int temp = arr[i];
        arr[i] = arr[size - 1 - i];
        arr[size - 1 - i] = temp;
    }
}

bool compareArrays(int arr1[], int size1, int arr2[], int size2)
{
    if (size1 != size2)
    {
        return false;
    }
    for (int i = 0; i < size1; i++)
    {
        if (arr1[i] != arr2[i])
        {
            return false;
        }
    }
    return true;
}

int main()
{
    int arr1[MAX_SIZE], arr2[MAX_SIZE];
    int size1 = 0, size2 = 0;
    int choice, element, index;

    do
    {
        printf("\nArray Operations Menu:\n");
        printf("1. Read and Display Array\n");
        printf("2. Insert Element\n");
        printf("3. Delete Element\n");
        printf("4. Append Array\n");
        printf("5. Reverse Array\n");
        printf("6. Compare Arrays\n");
        printf("0. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice)
        {
        case 1:
            readArray(arr1, &size1);
            displayArray(arr1, size1);
            break;
        case 2:
            printf("Enter element to insert: ");
            scanf("%d", &element);
            printf("Enter index: ");
            scanf("%d", &index);
            insertElement(arr1, &size1, element, index);
            displayArray(arr1, size1);
            break;
        case 3:
            printf("Enter index to delete: ");
            scanf("%d", &index);
            deleteElement(arr1, &size1, index);
            displayArray(arr1, size1);
            break;
        case 4:
            printf("Enter second array:\n");
            readArray(arr2, &size2);
            appendArray(arr1, &size1, arr2, size2);
            displayArray(arr1, size1);
            break;
        case 5:
            reverseArray(arr1, size1);
            displayArray(arr1, size1);
            break;
        case 6:
            printf("Enter second array:\n");
            readArray(arr2, &size2);
            if (compareArrays(arr1, size1, arr2, size2))
            {
                printf("Arrays are equal.\n");
            }
            else
            {
                printf("Arrays are not equal.\n");
            }
            break;
        case 0:
            printf("Exiting program.\n");
            break;
        default:
            printf("Invalid choice. Please try again.\n");
        }
    } while (choice != 0);

    return 0;
}