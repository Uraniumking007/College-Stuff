#include <stdio.h>
#include <stdlib.h>

int factorial_recursive(int n)
{
    if (n == 0 || n == 1)
    {
        return 1;
    }
    return n * factorial_recursive(n - 1);
}

int main(int argc, char const *argv[])
{
    int n;
    printf("Enter a positive integer: ");
    scanf("%d", &n);
    int result = factorial_recursive(n);
    printf("Factorial of %d = %d\n", n, result);
    return 0;
}
