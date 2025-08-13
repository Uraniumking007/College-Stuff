#include <stdio.h>
#include <stdlib.h>
#include <time.h>

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
    clock_t start = clock();
    int result = factorial(n);
    clock_t end = clock();
    double time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Factorial of %d = %d\n", n, result);
    printf("Time taken: %f seconds\n", time_taken);
    return 0;
}
