#include <stdio.h>
#include <stdlib.h>
#include <time.h>

typedef struct { int u, v, w; } Edge;

typedef struct { int parent; int rank; } Subset;

static int cmp_edges(const void *a, const void *b)
{
    const Edge *ea = (const Edge *)a;
    const Edge *eb = (const Edge *)b;
    return (ea->w > eb->w) - (ea->w < eb->w);
}

static int find_set(Subset *subsets, int i)
{
    if (subsets[i].parent != i)
        subsets[i].parent = find_set(subsets, subsets[i].parent);
    return subsets[i].parent;
}

static void union_sets(Subset *subsets, int x, int y)
{
    int xroot = find_set(subsets, x);
    int yroot = find_set(subsets, y);
    if (xroot == yroot) return;
    if (subsets[xroot].rank < subsets[yroot].rank)
        subsets[xroot].parent = yroot;
    else if (subsets[xroot].rank > subsets[yroot].rank)
        subsets[yroot].parent = xroot;
    else
    {
        subsets[yroot].parent = xroot;
        subsets[xroot].rank++;
    }
}

int main()
{
    int V, E;
    printf("Enter number of vertices and edges: ");
    if (scanf("%d %d", &V, &E) != 2 || V <= 0 || E < 0) { printf("Invalid input.\n"); return 1; }

    Edge *edges = (Edge *)malloc(sizeof(Edge) * (size_t)E);
    if (!edges) { printf("Memory allocation failed.\n"); return 1; }

    printf("Enter edges (u v w) with vertices 0..%d:\n", V - 1);
    for (int i = 0; i < E; i++)
    {
        if (scanf("%d %d %d", &edges[i].u, &edges[i].v, &edges[i].w) != 3)
        {
            printf("Invalid edge.\n");
            free(edges);
            return 1;
        }
    }

    clock_t start = clock();
    qsort(edges, (size_t)E, sizeof(Edge), cmp_edges);

    Subset *subsets = (Subset *)malloc(sizeof(Subset) * (size_t)V);
    for (int v = 0; v < V; v++) { subsets[v].parent = v; subsets[v].rank = 0; }

    int edge_count = 0;
    int total_weight = 0;
    printf("Edges in MST (u - v : weight):\n");
    for (int i = 0; i < E && edge_count < V - 1; i++)
    {
        int u = edges[i].u;
        int v = edges[i].v;
        int set_u = find_set(subsets, u);
        int set_v = find_set(subsets, v);
        if (set_u != set_v)
        {
            printf("%d - %d : %d\n", u, v, edges[i].w);
            total_weight += edges[i].w;
            union_sets(subsets, set_u, set_v);
            edge_count++;
        }
    }
    clock_t end = clock();

    printf("Total weight: %d\n", total_weight);
    double elapsed = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Time taken: %.9f seconds\n", elapsed);

    free(subsets);
    free(edges);
    return 0;
}


