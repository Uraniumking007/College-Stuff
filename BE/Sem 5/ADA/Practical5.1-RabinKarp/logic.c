#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// Rabin-Karp with rolling hash (base d, mod q)

static void rabin_karp(const char *text, const char *pattern, int d, int q)
{
    int n = (int)strlen(text);
    int m = (int)strlen(pattern);
    if (m == 0 || n < m) { printf("No matches.\n"); return; }

    int h = 1;
    for (int i = 0; i < m - 1; i++) h = (h * d) % q;

    int p = 0; // hash value for pattern
    int t = 0; // hash value for text window
    for (int i = 0; i < m; i++)
    {
        p = (d * p + (unsigned char)pattern[i]) % q;
        t = (d * t + (unsigned char)text[i]) % q;
    }

    int found = 0;
    for (int i = 0; i <= n - m; i++)
    {
        if (p == t)
        {
            int match = 1;
            for (int j = 0; j < m; j++)
            {
                if (text[i + j] != pattern[j]) { match = 0; break; }
            }
            if (match)
            {
                if (!found) { printf("Matches at indices: "); found = 1; }
                printf("%d ", i);
            }
        }
        if (i < n - m)
        {
            t = (d * (t - (unsigned char)text[i] * h) + (unsigned char)text[i + 1]) % q;
            if (t < 0) t += q;
        }
    }
    if (!found) printf("No matches.");
    printf("\n");
}

int main()
{
    char text[4096];
    char pattern[1024];
    printf("Enter text: ");
    if (!fgets(text, sizeof(text), stdin)) return 1;
    size_t len = strlen(text);
    if (len && text[len - 1] == '\n') text[len - 1] = '\0';
    printf("Enter pattern: ");
    if (!fgets(pattern, sizeof(pattern), stdin)) return 1;
    len = strlen(pattern);
    if (len && pattern[len - 1] == '\n') pattern[len - 1] = '\0';

    clock_t start = clock();
    rabin_karp(text, pattern, 256, 101); // base 256, prime 101
    clock_t end = clock();
    double elapsed = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Time taken: %.9f seconds\n", elapsed);
    return 0;
}


