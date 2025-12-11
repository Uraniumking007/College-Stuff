#include <stdio.h>
#include <stdlib.h>
#include <time.h>

typedef struct Node { int v; struct Node *next; } Node;

static void add_edge(Node **adj, int u, int v)
{
    Node *nv = (Node *)malloc(sizeof(Node));
    nv->v = v; nv->next = adj[u]; adj[u] = nv;
}

static void bfs(Node **adj, int V, int start)
{
    int *visited = (int *)calloc((size_t)V, sizeof(int));
    int *queue = (int *)malloc(sizeof(int) * (size_t)V);
    int front = 0, rear = 0;

    visited[start] = 1;
    queue[rear++] = start;
    printf("BFS order: ");

    while (front < rear)
    {
        int u = queue[front++];
        printf("%d ", u);
        for (Node *p = adj[u]; p != NULL; p = p->next)
        {
            int w = p->v;
            if (!visited[w])
            {
                visited[w] = 1;
                queue[rear++] = w;
            }
        }
    }
    printf("\n");

    free(queue);
    free(visited);
}

int main()
{
    int V, E;
    printf("Enter number of vertices and edges: ");
    if (scanf("%d %d", &V, &E) != 2 || V <= 0 || E < 0) { printf("Invalid input.\n"); return 1; }
    Node **adj = (Node **)calloc((size_t)V, sizeof(Node *));
    printf("Enter %d edges (u v) directed or undirected as desired:\n", E);
    for (int i = 0; i < E; i++)
    {
        int u, v; if (scanf("%d %d", &u, &v) != 2) { printf("Invalid edge.\n"); return 1; }
        if (u < 0 || u >= V || v < 0 || v >= V) { printf("Vertex out of range.\n"); return 1; }
        add_edge(adj, u, v);
        // For undirected, also add reverse; uncomment if needed:
        // add_edge(adj, v, u);
    }
    int start;
    printf("Enter start vertex: ");
    if (scanf("%d", &start) != 1 || start < 0 || start >= V) { printf("Invalid start.\n"); return 1; }

    clock_t begin = clock();
    bfs(adj, V, start);
    clock_t finish = clock();
    double elapsed = (double)(finish - begin) / CLOCKS_PER_SEC;
    printf("Time taken: %.9f seconds\n", elapsed);

    for (int i = 0; i < V; i++)
    {
        Node *p = adj[i];
        while (p) { Node *n = p->next; free(p); p = n; }
    }
    free(adj);
    return 0;
}


