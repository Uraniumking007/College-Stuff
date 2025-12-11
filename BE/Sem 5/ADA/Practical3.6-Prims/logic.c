#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <time.h>

static int min_key(const int *key, const int *mstSet, int V)
{
    int min = INT_MAX, min_index = -1;
    for (int v = 0; v < V; v++)
    {
        if (!mstSet[v] && key[v] < min) { min = key[v]; min_index = v; }
    }
    return min_index;
}

// Adjacency matrix Prim's (O(V^2))
static void prim_mst(int **graph, int V)
{
    int *parent = (int *)malloc(sizeof(int) * (size_t)V);
    int *key = (int *)malloc(sizeof(int) * (size_t)V);
    int *mstSet = (int *)calloc((size_t)V, sizeof(int));

    for (int i = 0; i < V; i++) key[i] = INT_MAX, parent[i] = -1;
    key[0] = 0;

    for (int count = 0; count < V - 1; count++)
    {
        int u = min_key(key, mstSet, V);
        mstSet[u] = 1;
        for (int v = 0; v < V; v++)
        {
            if (graph[u][v] && !mstSet[v] && graph[u][v] < key[v])
            {
                parent[v] = u;
                key[v] = graph[u][v];
            }
        }
    }

    int total = 0;
    printf("Edges in MST (u - v : weight):\n");
    for (int i = 1; i < V; i++)
    {
        printf("%d - %d : %d\n", parent[i], i, graph[i][parent[i]]);
        total += graph[i][parent[i]];
    }
    printf("Total weight: %d\n", total);

    free(parent);
    free(key);
    free(mstSet);
}

int main()
{
    int V;
    printf("Enter number of vertices: ");
    if (scanf("%d", &V) != 1 || V <= 0) { printf("Invalid V.\n"); return 1; }

    int **graph = (int **)malloc(sizeof(int *) * (size_t)V);
    for (int i = 0; i < V; i++) graph[i] = (int *)malloc(sizeof(int) * (size_t)V);

    printf("Enter adjacency matrix (%d x %d), 0 for no edge:\n", V, V);
    for (int i = 0; i < V; i++)
        for (int j = 0; j < V; j++)
            if (scanf("%d", &graph[i][j]) != 1) { printf("Invalid input.\n"); return 1; }

    clock_t start = clock();
    prim_mst(graph, V);
    clock_t end = clock();
    double elapsed = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Time taken: %.9f seconds\n", elapsed);

    for (int i = 0; i < V; i++) free(graph[i]);
    free(graph);
    return 0;
}


