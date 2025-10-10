#include <stdio.h>
#include <stdlib.h>

struct Node
{
    int data;
    struct Node *next;
};

struct Queue
{
    struct Node *front, *rear;
};

struct Node *newNode(int k)
{
    struct Node *temp = (struct Node *)malloc(sizeof(struct Node));
    temp->data = k;
    temp->next = NULL;
    return temp;
}

struct Queue *createQueue()
{
    struct Queue *q = (struct Queue *)malloc(sizeof(struct Queue));
    q->front = q->rear = NULL;
    return q;
}

void enqueue(struct Queue *q, int k)
{
    struct Node *temp = newNode(k);

    if (q->rear == NULL)
    {
        q->front = q->rear = temp;
        return;
    }
    q->rear->next = temp;
    q->rear = temp;
}

void dequeue(struct Queue *q)
{
    if (q->front == NULL)
        return;

    struct Node *temp = q->front;
    q->front = q->front->next;

    if (q->front == NULL)
        q->rear = NULL;

    free(temp);
}

void displayQueue(struct Queue *q)
{
    struct Node *temp = q->front;
    while (temp != NULL)
    {
        printf("%d -> ", temp->data);
        temp = temp->next;
    }
    printf("NULL\n");
}

void main()
{
    struct Queue *q = createQueue();
    enqueue(q, 10);
    enqueue(q, 20);
    enqueue(q, 30);
    enqueue(q, 40);

    printf("Queue: ");
    displayQueue(q);

    dequeue(q);
    printf("Queue after dequeue: ");
    displayQueue(q);
}