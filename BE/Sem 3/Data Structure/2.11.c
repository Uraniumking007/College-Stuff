#include <stdio.h>
#include <stdlib.h>

struct Node
{
    int data;
    struct Node *prev;
    struct Node *next;
};

void insertFront(struct Node **head, int data)
{
    struct Node *newNode = (struct Node *)malloc(sizeof(struct Node));
    newNode->data = data;
    newNode->prev = NULL;
    newNode->next = *head;
    if (*head != NULL)
    {
        (*head)->prev = newNode;
    }
    *head = newNode;
}

void insertEnd(struct Node **head, int data)
{
    struct Node *newNode = (struct Node *)malloc(sizeof(struct Node));
    struct Node *temp = *head;
    newNode->data = data;
    newNode->next = NULL;
    if (*head == NULL)
    {
        newNode->prev = NULL;
        *head = newNode;
        return;
    }
    while (temp->next != NULL)
    {
        temp = temp->next;
    }
    temp->next = newNode;
    newNode->prev = temp;
}

void deleteFirst(struct Node **head)
{
    if (*head == NULL)
    {
        printf("List is empty.\n");
        return;
    }
    struct Node *temp = *head;
    *head = (*head)->next;
    if (*head != NULL)
    {
        (*head)->prev = NULL;
    }
    free(temp);
}

void deleteBeforePosition(struct Node **head, int position)
{
    if (*head == NULL || position <= 1)
    {
        printf("Invalid position or list is empty.\n");
        return;
    }
    struct Node *temp = *head;
    for (int i = 1; temp != NULL && i < position - 1; i++)
    {
        temp = temp->next;
    }
    if (temp == NULL || temp->prev == NULL)
    {
        printf("No node exists before the specified position.\n");
        return;
    }
    struct Node *nodeToDelete = temp->prev;
    if (nodeToDelete->prev != NULL)
    {
        nodeToDelete->prev->next = temp;
    }
    else
    {
        *head = temp;
    }
    temp->prev = nodeToDelete->prev;
    free(nodeToDelete);
}

void printList(struct Node *node)
{
    while (node != NULL)
    {
        printf("%d ", node->data);
        node = node->next;
    }
    printf("\n");
}

void main()
{
    struct Node *head = NULL;
    int choice, data, position;

    while (1)
    {
        printf("\nMenu:\n");
        printf("1. Insert at front\n");
        printf("2. Insert at end\n");
        printf("3. Delete first node\n");
        printf("4. Delete node before position\n");
        printf("5. Print list\n");
        printf("6. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice)
        {
        case 1:
            printf("Enter data to insert at front: ");
            scanf("%d", &data);
            insertFront(&head, data);
            break;
        case 2:
            printf("Enter data to insert at end: ");
            scanf("%d", &data);
            insertEnd(&head, data);
            break;
        case 3:
            deleteFirst(&head);
            break;
        case 4:
            printf("Enter position before which to delete node: ");
            scanf("%d", &position);
            deleteBeforePosition(&head, position);
            break;
        case 5:
            printf("Doubly linked list: ");
            printList(head);
            break;
        case 6:
            exit(0);
        default:
            printf("Invalid choice. Please try again.\n");
        }
    }
}