#include <stdio.h>
#include <stdlib.h>
#include <time.h>

static int max(int a, int b) { return a > b ? a : b; }

static int knapsack_01(int capacity, const int *weights, const int *values, int n)
{
    int **dp = (int **)malloc((size_t)(n + 1) * sizeof(int *));
    for (int i = 0; i <= n; i++)
    {
        dp[i] = (int *)malloc((size_t)(capacity + 1) * sizeof(int));
    }

    for (int i = 0; i <= n; i++)
    {
        for (int w = 0; w <= capacity; w++)
        {
            if (i == 0 || w == 0) dp[i][w] = 0;
            else if (weights[i - 1] <= w)
                dp[i][w] = max(values[i - 1] + dp[i - 1][w - weights[i - 1]], dp[i - 1][w]);
            else
                dp[i][w] = dp[i - 1][w];
        }
    }

    int result = dp[n][capacity];
    for (int i = 0; i <= n; i++) free(dp[i]);
    free(dp);
    return result;
}

int main()
{
    int n;
    printf("Enter number of items: ");
    if (scanf("%d", &n) != 1 || n <= 0)
    {
        printf("Invalid n.\n");
        return 1;
    }

    int capacity;
    printf("Enter knapsack capacity: ");
    if (scanf("%d", &capacity) != 1 || capacity < 0)
    {
        printf("Invalid capacity.\n");
        return 1;
    }

    int *weights = (int *)malloc(sizeof(int) * (size_t)n);
    int *values = (int *)malloc(sizeof(int) * (size_t)n);
    if (!weights || !values)
    {
        printf("Memory allocation failed.\n");
        free(weights);
        free(values);
        return 1;
    }

    printf("Enter weights of %d items:\n", n);
    for (int i = 0; i < n; i++) if (scanf("%d", &weights[i]) != 1) { printf("Invalid input.\n"); free(weights); free(values); return 1; }
    printf("Enter values of %d items:\n", n);
    for (int i = 0; i < n; i++) if (scanf("%d", &values[i]) != 1) { printf("Invalid input.\n"); free(weights); free(values); return 1; }

    clock_t start_time = clock();
    int best_value = knapsack_01(capacity, weights, values, n);
    clock_t end_time = clock();

    double elapsed_seconds = (double)(end_time - start_time) / CLOCKS_PER_SEC;
    printf("Maximum achievable value: %d\n", best_value);
    printf("Time taken: %.9f seconds\n", elapsed_seconds);

    free(weights);
    free(values);
    return 0;
}


