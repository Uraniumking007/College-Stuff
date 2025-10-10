#include <stdio.h>
#include <stdlib.h>

int main()
{
    int *array = (int *)malloc(5 * sizeof(int));
    if (array == NULL)
    {
        printf("Memory allocation failed using malloc.\n");
        return 1;
    }

    for (int i = 0; i < 5; i++)
    {
        array[i] = i + 1;
    }

    printf("Array allocated using malloc:\n");
    for (int i = 0; i < 5; i++)
    {
        printf("%d ", array[i]);
    }
    printf("\n");

    int *newArray = (int *)calloc(10, sizeof(int));
    if (newArray == NULL)
    {
        printf("Memory allocation failed using calloc.\n");
        free(array);
        return 1;
    }

    for (int i = 0; i < 10; i++)
    {
        newArray[i] = (i + 1) * 10;
    }

    printf("Array allocated using calloc:\n");
    for (int i = 0; i < 10; i++)
    {
        printf("%d ", newArray[i]);
    }
    printf("\n");

    int *resizedArray = (int *)realloc(newArray, 15 * sizeof(int));
    if (resizedArray == NULL)
    {
        printf("Memory reallocation failed.\n");
        free(newArray);
        free(array);
        return 1;
    }

    for (int i = 10; i < 15; i++)
    {
        resizedArray[i] = (i + 1) * 20;
    }

    printf("Resized array using realloc:\n");
    for (int i = 0; i < 15; i++)
    {
        printf("%d ", resizedArray[i]);
    }
    printf("\n");

    free(resizedArray);
    free(array);

    return 0;
}
