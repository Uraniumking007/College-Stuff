#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <time.h>

static int min(int a, int b) { return a < b ? a : b; }

static int matrix_chain_order(const int *p, int n)
{
    // p has length n+1, matrices A_i are p[i-1] x p[i]
    int **m = (int **)malloc((size_t)(n + 1) * sizeof(int *));
    for (int i = 0; i <= n; i++) m[i] = (int *)malloc((size_t)(n + 1) * sizeof(int));

    for (int i = 1; i <= n; i++) m[i][i] = 0;

    for (int L = 2; L <= n; L++)
    {
        for (int i = 1; i <= n - L + 1; i++)
        {
            int j = i + L - 1;
            m[i][j] = INT_MAX;
            for (int k = i; k <= j - 1; k++)
            {
                long cost = (long)m[i][k] + m[k + 1][j] + (long)p[i - 1] * p[k] * p[j];
                if (cost < m[i][j]) m[i][j] = (int)cost;
            }
        }
    }

    int result = m[1][n];
    for (int i = 0; i <= n; i++) free(m[i]);
    free(m);
    return result;
}

int main()
{
    int n;
    printf("Enter number of matrices: ");
    if (scanf("%d", &n) != 1 || n <= 0)
    {
        printf("Invalid n.\n");
        return 1;
    }

    // We need n+1 dimensions
    int *p = (int *)malloc(sizeof(int) * (size_t)(n + 1));
    if (!p)
    {
        printf("Memory allocation failed.\n");
        return 1;
    }
    printf("Enter %d dimensions (p0 p1 ... pn):\n", n + 1);
    for (int i = 0; i <= n; i++) if (scanf("%d", &p[i]) != 1) { printf("Invalid input.\n"); free(p); return 1; }

    clock_t start_time = clock();
    int min_mults = matrix_chain_order(p, n);
    clock_t end_time = clock();

    double elapsed_seconds = (double)(end_time - start_time) / CLOCKS_PER_SEC;
    printf("Minimum number of multiplications: %d\n", min_mults);
    printf("Time taken: %.9f seconds\n", elapsed_seconds);

    free(p);
    return 0;
}


