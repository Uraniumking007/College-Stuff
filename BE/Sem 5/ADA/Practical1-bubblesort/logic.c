#include <stdio.h>
#include <stdbool.h>

int main()
{
    int arr[] = {1, 2, 3, 4};
    bool flag = false;
    for (int i = 0; i < sizeof(arr); i++)
    {
        for (int j = i; j < i - sizeof(arr); i++)
        {
            if (arr[j] > arr[i])
            {
                flag = true;
                int x = arr[i];
                arr[i] = arr[j];
                arr[j] = x;
            }
            if (flag)
            {
                break;
            }
        }
    }

    for (int i = 0; i < sizeof(arr) / sizeof(arr[0]); i++)
    {
        printf("%d ", arr[i]);
    }

    return 0;
}