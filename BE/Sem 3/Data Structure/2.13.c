#include <stdio.h>
#define MAX 100

int queue[MAX];
int front = -1, rear = -1;

void insert(int element)
{
    if (rear == MAX - 1)
    {
        printf("Queue Overflow\n");
        return;
    }
    if (front == -1)
    {
        front = 0;
    }
    queue[++rear] = element;
    printf("Inserted %d\n", element);
}

void delete()
{
    if (front == -1 || front > rear)
    {
        printf("Queue Underflow\n");
        return;
    }
    printf("Deleted %d\n", queue[front++]);
    if (front > rear)
    {
        front = rear = -1;
    }
}

void display()
{
    if (front == -1)
    {
        printf("Queue is empty\n");
        return;
    }
    printf("Queue elements are:\n");
    for (int i = front; i <= rear; i++)
    {
        printf("%d ", queue[i]);
    }
    printf("\n");
}

int main()
{
    int choice, element;
    while (1)
    {
        printf("\nQueue Operations:\n");
        printf("1. Insert\n");
        printf("2. Delete\n");
        printf("3. Display\n");
        printf("4. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);
        switch (choice)
        {
        case 1:
            printf("Enter element to insert: ");
            scanf("%d", &element);
            insert(element);
            break;
        case 2:
            delete ();
            break;
        case 3:
            display();
            break;
        case 4:
            return 0;
        default:
            printf("Invalid choice\n");
        }
    }
    return 0;
}