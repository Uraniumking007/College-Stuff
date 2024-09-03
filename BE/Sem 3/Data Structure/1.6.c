#include <stdio.h>

void callByValue(int x);
void callByReference(int *x);

int main()
{
    int num = 10;
    int *ptr = &num;

    printf("Value of num: %d\n", num);
    printf("Address of num: %p\n", (void *)&num);
    printf("Value of ptr: %p\n", (void *)ptr);
    printf("Value pointed to by ptr: %d\n", *ptr);

    printf("\nDemonstrating Call by Value:\n");
    printf("Before call by value, num = %d\n", num);
    callByValue(num);
    printf("After call by value, num = %d\n", num);

    printf("\nDemonstrating Call by Reference:\n");
    printf("Before call by reference, num = %d\n", num);
    callByReference(&num);
    printf("After call by reference, num = %d\n", num);

    return 0;
}

void callByValue(int x)
{
    x = x * 2;
    printf("Inside callByValue function, x = %d\n", x);
}

void callByReference(int *x)
{
    *x = *x * 2;
    printf("Inside callByReference function, *x = %d\n", *x);
}