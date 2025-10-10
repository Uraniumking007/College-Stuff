#include <stdio.h>
#include <stdlib.h>
#include <time.h>

typedef struct { double ratio; int weight; int value; } Item;

static int cmp_items_desc(const void *a, const void *b)
{
    const Item *ia = (const Item *)a;
    const Item *ib = (const Item *)b;
    if (ia->ratio < ib->ratio) return 1;
    if (ia->ratio > ib->ratio) return -1;
    return 0;
}

int main()
{
    int n;
    printf("Enter number of items: ");
    if (scanf("%d", &n) != 1 || n <= 0) { printf("Invalid n.\n"); return 1; }

    int capacity;
    printf("Enter knapsack capacity: ");
    if (scanf("%d", &capacity) != 1 || capacity < 0) { printf("Invalid capacity.\n"); return 1; }

    Item *items = (Item *)malloc(sizeof(Item) * (size_t)n);
    if (!items) { printf("Memory allocation failed.\n"); return 1; }

    int *weights = (int *)malloc(sizeof(int) * (size_t)n);
    int *values = (int *)malloc(sizeof(int) * (size_t)n);
    if (!weights || !values) { printf("Memory allocation failed.\n"); free(items); free(weights); free(values); return 1; }

    printf("Enter weights of %d items:\n", n);
    for (int i = 0; i < n; i++) if (scanf("%d", &weights[i]) != 1 || weights[i] < 0) { printf("Invalid input.\n"); free(items); free(weights); free(values); return 1; }
    printf("Enter values of %d items:\n", n);
    for (int i = 0; i < n; i++) if (scanf("%d", &values[i]) != 1 || values[i] < 0) { printf("Invalid input.\n"); free(items); free(weights); free(values); return 1; }

    for (int i = 0; i < n; i++) { items[i].weight = weights[i]; items[i].value = values[i]; items[i].ratio = items[i].weight == 0 ? 0.0 : (double)items[i].value / items[i].weight; }

    clock_t start = clock();
    qsort(items, (size_t)n, sizeof(Item), cmp_items_desc);

    double total_value = 0.0;
    int remaining = capacity;
    for (int i = 0; i < n && remaining > 0; i++)
    {
        if (items[i].weight <= remaining)
        {
            remaining -= items[i].weight;
            total_value += items[i].value;
        }
        else
        {
            double fraction = (double)remaining / items[i].weight;
            total_value += items[i].value * fraction;
            remaining = 0;
        }
    }
    clock_t end = clock();

    double elapsed = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Maximum value (fractional): %.6f\n", total_value);
    printf("Time taken: %.9f seconds\n", elapsed);

    free(items);
    free(weights);
    free(values);
    return 0;
}


