#include <stdio.h>
#include <stdlib.h>

int factorial(int n)
{
    int result = 1;
    for (size_t i = 1; i <= n; i++)
    {
        result *= i;
    }
    return result;
}

int main()
{
    int n;
    printf("Enter a positive integer: ");
    scanf("%d", &n);
    int result = factorial(n);
    printf("Factorial of %d = %d\n", n, result);
    return 0;
}
