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

int main()
{
    struct Node *head = NULL;

    insertFront(&head, 10);
    insertFront(&head, 20);
    insertEnd(&head, 30);
    insertEnd(&head, 40);

    printf("Doubly linked list: ");
    printList(head);

    deleteFirst(&head);
    printf("After deleting first node: ");
    printList(head);

    deleteBeforePosition(&head, 3);
    printf("After deleting node before position 3: ");
    printList(head);

    return 0;
}