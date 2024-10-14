#include <stdio.h>
#include <stdlib.h>

struct Node
{
    int data;
    struct Node *next;
    struct Node *prev;
};

struct Node *head = NULL;
struct Node *tail = NULL;

void insertAtFront(int data)
{
    struct Node *newNode = (struct Node *)malloc(sizeof(struct Node));
    newNode->data = data;
    newNode->next = head;
    newNode->prev = tail;
    head = newNode;
    if (tail == NULL)
    {
        tail = newNode;
    }
}

void insertAtEnd(int data)
{
    struct Node *newNode = (struct Node *)malloc(sizeof(struct Node));
    newNode->data = data;
    newNode->next = NULL;
    newNode->prev = NULL;

    if (head == NULL)
    {
        head = newNode;
        tail = newNode;
    }
    else
    {
        struct Node *temp = head;
        while (temp->next != NULL)
        {
            temp = temp->next;
        }
        temp->next = newNode;
        newNode->prev = temp;
        tail = newNode;
    }
}

void deleteFirstNode()
{
    if (head != NULL)
    {
        struct Node *temp = head;
        head = head->next;
        tail = head->prev;
        free(temp);
    }
}

void deleteBeforePosition(int pos)
{
    if (pos <= 1 || head == NULL || head->next == NULL)
    {
        printf("Invalid position or list is too short.\n");
        return;
    }
    struct Node *temp = head;
    if (pos == 2)
    {
        head = head->next;
        tail = head->prev;
        free(temp);
        return;
    }
    struct Node *prev = NULL;
    for (int i = 1; i < pos - 1 && temp->next != NULL; i++)
    {
        prev = temp;
        temp = temp->next;
    }
    if (temp->next != NULL)
    {
        prev->next = temp->next;
        prev->prev = temp->prev;
        free(temp);
    }
    else
    {
        printf("Position out of bounds.\n");
    }
}

void deleteAfterPosition(int pos)
{
    struct Node *temp = head;
    for (int i = 1; i < pos && temp != NULL; i++)
    {
        temp = temp->next;
    }
    if (temp != NULL && temp->next != NULL)
    {
        struct Node *nodeToDelete = temp->next;
        temp->next = nodeToDelete->next;
        temp->prev = nodeToDelete->prev;
        free(nodeToDelete);
    }
    else
    {
        printf("Position out of bounds or no node to delete.\n");
    }
}

void displayList()
{
    struct Node *temp = head;
    while (temp != NULL)
    {
        printf("%d -> ", temp->data);
        temp = temp->next;
    }
    printf("NULL\n");
}

int main()
{
    int choice, data, pos;
    while (1)
    {
        printf("\nMenu:\n");
        printf("1. Insert at front\n");
        printf("2. Insert at end\n");
        printf("3. Delete first node\n");
        printf("4. Delete before position\n");
        printf("5. Display list\n");
        printf("6. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);
        switch (choice)
        {
        case 1:
            printf("Enter data: ");
            scanf("%d", &data);
            insertAtFront(data);
            break;
        case 2:
            printf("Enter data: ");
            scanf("%d", &data);
            insertAtEnd(data);
            break;
        case 3:
            deleteFirstNode();
            break;
        case 4:
            printf("Enter position: ");
            scanf("%d", &pos);
            deleteBeforePosition(pos);
            break;
        case 5:
            displayList();

            break;
        case 6:
            exit(0);
        default:
            printf("Invalid choice.\n");
        }
    }
    return 0;
}