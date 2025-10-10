#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

static int max(int a, int b) { return a > b ? a : b; }

static int lcs_length(const char *X, const char *Y, char **out_sequence)
{
    int m = (int)strlen(X);
    int n = (int)strlen(Y);
    int **L = (int **)malloc((size_t)(m + 1) * sizeof(int *));
    for (int i = 0; i <= m; i++) L[i] = (int *)calloc((size_t)(n + 1), sizeof(int));

    for (int i = 1; i <= m; i++)
    {
        for (int j = 1; j <= n; j++)
        {
            if (X[i - 1] == Y[j - 1]) L[i][j] = L[i - 1][j - 1] + 1;
            else L[i][j] = max(L[i - 1][j], L[i][j - 1]);
        }
    }

    int length = L[m][n];
    if (out_sequence)
    {
        char *seq = (char *)malloc((size_t)length + 1);
        seq[length] = '\0';
        int i = m, j = n, idx = length - 1;
        while (i > 0 && j > 0)
        {
            if (X[i - 1] == Y[j - 1]) { seq[idx--] = X[i - 1]; i--; j--; }
            else if (L[i - 1][j] >= L[i][j - 1]) i--;
            else j--;
        }
        *out_sequence = seq;
    }

    for (int i = 0; i <= m; i++) free(L[i]);
    free(L);
    return length;
}

int main()
{
    char X[1024];
    char Y[1024];
    printf("Enter first string: ");
    if (scanf("%1023s", X) != 1) { printf("Invalid input.\n"); return 1; }
    printf("Enter second string: ");
    if (scanf("%1023s", Y) != 1) { printf("Invalid input.\n"); return 1; }

    clock_t start = clock();
    char *sequence = NULL;
    int length = lcs_length(X, Y, &sequence);
    clock_t end = clock();

    double elapsed = (double)(end - start) / CLOCKS_PER_SEC;
    printf("LCS length: %d\n", length);
    if (sequence)
    {
        printf("LCS: %s\n", sequence);
        free(sequence);
    }
    printf("Time taken: %.9f seconds\n", elapsed);
    return 0;
}


