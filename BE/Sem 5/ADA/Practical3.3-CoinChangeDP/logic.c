#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <time.h>

// Computes minimum coins to make amount and number of ways to make amount
// using unbounded coin change (infinite coins of each denomination)

static int min(int a, int b) { return a < b ? a : b; }

static int min_coins_unbounded(int amount, const int *coins, int n)
{
    int *dp = (int *)malloc((size_t)(amount + 1) * sizeof(int));
    for (int i = 0; i <= amount; i++) dp[i] = INT_MAX / 2; // avoid overflow
    dp[0] = 0;
    for (int i = 0; i < n; i++)
    {
        int coin = coins[i];
        for (int a = coin; a <= amount; a++)
        {
            dp[a] = min(dp[a], 1 + dp[a - coin]);
        }
    }
    int ans = dp[amount];
    free(dp);
    return ans >= INT_MAX / 4 ? -1 : ans;
}

static long long count_ways_unbounded(int amount, const int *coins, int n)
{
    long long *ways = (long long *)calloc((size_t)(amount + 1), sizeof(long long));
    if (!ways) return 0;
    ways[0] = 1;
    for (int i = 0; i < n; i++)
    {
        int coin = coins[i];
        for (int a = coin; a <= amount; a++)
        {
            ways[a] += ways[a - coin];
        }
    }
    long long ans = ways[amount];
    free(ways);
    return ans;
}

int main()
{
    int n;
    printf("Enter number of coin denominations: ");
    if (scanf("%d", &n) != 1 || n <= 0)
    {
        printf("Invalid n.\n");
        return 1;
    }

    int *coins = (int *)malloc(sizeof(int) * (size_t)n);
    if (!coins)
    {
        printf("Memory allocation failed.\n");
        return 1;
    }
    printf("Enter %d coin values:\n", n);
    for (int i = 0; i < n; i++) if (scanf("%d", &coins[i]) != 1 || coins[i] <= 0) { printf("Invalid coin.\n"); free(coins); return 1; }

    int amount;
    printf("Enter amount: ");
    if (scanf("%d", &amount) != 1 || amount < 0)
    {
        printf("Invalid amount.\n");
        free(coins);
        return 1;
    }

    clock_t start = clock();
    int min_coins = min_coins_unbounded(amount, coins, n);
    long long ways = count_ways_unbounded(amount, coins, n);
    clock_t end = clock();

    double elapsed = (double)(end - start) / CLOCKS_PER_SEC;
    if (min_coins >= 0) printf("Minimum coins needed: %d\n", min_coins);
    else printf("Amount cannot be formed with given coins.\n");
    printf("Number of ways: %lld\n", ways);
    printf("Time taken: %.9f seconds\n", elapsed);

    free(coins);
    return 0;
}


