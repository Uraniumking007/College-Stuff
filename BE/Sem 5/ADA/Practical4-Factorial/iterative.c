#include <stdio.h>
#include <stdlib.h>
#include <time.h>

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
    int time_taken;
    printf("Enter a positive integer: ");
    scanf("%d", &n);

    clock_t start = clock();
    int result = factorial_recursive(n);
    clock_t end = clock();

    time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;

    printf("Factorial of %d = %d\n", n, result);
    printf("Time taken: %d seconds\n", time_taken);
    return 0;
}
