#include <stdio.h>
#include <stdlib.h>

struct Node
{
    int data;
    struct Node *left;
    struct Node *right;
};

struct Node *newNode(int data)
{
    struct Node *node = (struct Node *)malloc(sizeof(struct Node));
    node->data = data;
    node->left = NULL;
    node->right = NULL;
    return node;
}

void inorderRecursive(struct Node *root)
{
    if (root == NULL)
        return;
    inorderRecursive(root->left);
    printf("%d ", root->data);
    inorderRecursive(root->right);
}

void preorderRecursive(struct Node *root)
{
    if (root == NULL)
        return;
    printf("%d ", root->data);
    preorderRecursive(root->left);
    preorderRecursive(root->right);
}

void postorderRecursive(struct Node *root)
{
    if (root == NULL)
        return;
    postorderRecursive(root->left);
    postorderRecursive(root->right);
    printf("%d ", root->data);
}

void inorderNonRecursive(struct Node *root)
{
    struct Node *stack[100];
    int top = -1;
    struct Node *current = root;

    while (current != NULL || top != -1)
    {
        while (current != NULL)
        {
            stack[++top] = current;
            current = current->left;
        }
        current = stack[top--];
        printf("%d ", current->data);
        current = current->right;
    }
}

void preorderNonRecursive(struct Node *root)
{
    if (root == NULL)
        return;
    struct Node *stack[100];
    int top = -1;
    stack[++top] = root;

    while (top != -1)
    {
        struct Node *current = stack[top--];
        printf("%d ", current->data);

        if (current->right)
            stack[++top] = current->right;
        if (current->left)
            stack[++top] = current->left;
    }
}

void postorderNonRecursive(struct Node *root)
{
    if (root == NULL)
        return;
    struct Node *stack1[100];
    struct Node *stack2[100];
    int top1 = -1, top2 = -1;
    stack1[++top1] = root;

    while (top1 != -1)
    {
        struct Node *current = stack1[top1--];
        stack2[++top2] = current;

        if (current->left)
            stack1[++top1] = current->left;
        if (current->right)
            stack1[++top1] = current->right;
    }

    while (top2 != -1)
    {
        struct Node *current = stack2[top2--];
        printf("%d ", current->data);
    }
}

void main()
{
    struct Node *root = newNode(1);
    root->left = newNode(2);
    root->right = newNode(3);
    root->left->left = newNode(4);
    root->left->right = newNode(5);
    root->right->left = newNode(6);
    root->right->right = newNode(7);

    printf("Recursive Inorder Traversal: ");
    inorderRecursive(root);
    printf("\n");

    printf("Non-Recursive Inorder Traversal: ");
    inorderNonRecursive(root);
    printf("\n");

    printf("Recursive Preorder Traversal: ");
    preorderRecursive(root);
    printf("\n");

    printf("Non-Recursive Preorder Traversal: ");
    preorderNonRecursive(root);
    printf("\n");

    printf("Recursive Postorder Traversal: ");
    postorderRecursive(root);
    printf("\n");

    printf("Non-Recursive Postorder Traversal: ");
    postorderNonRecursive(root);
    printf("\n");
}