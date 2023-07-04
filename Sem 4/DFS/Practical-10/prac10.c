#include <stdio.h>
#include <stdlib.h>

struct node
{
    int DATA;
    struct node *LPTR;
    struct node *RPTR;
} *ROOT = NULL;

struct node *create(struct node *ROOT, int value)
{
    if (ROOT == NULL)
    {
        struct node *new_node = (struct node *)malloc(sizeof(struct node));
        new_node->DATA = value;
        new_node->LPTR = NULL;
        new_node->RPTR = NULL;
        printf("%d is inserted\n", value);
        ROOT = new_node;
        return ROOT;
    }
    else if (value >= ROOT->DATA)
    {
        ROOT->RPTR = create(ROOT->RPTR, value);
        return ROOT;
    }
    else if (value <= ROOT->DATA)
    {
        ROOT->LPTR = create(ROOT->LPTR, value);
        return ROOT;
    }
}

void Preorder(struct node *ROOT)
{
    if (ROOT != NULL)
    {
        printf("%d,", ROOT->DATA);
        Preorder(ROOT->LPTR);
        Preorder(ROOT->RPTR);
    }
}

void Inorder(struct node *ROOT)
{
    if (ROOT != NULL)
    {
        Preorder(ROOT->LPTR);
        printf("%d,", ROOT->DATA);
        Preorder(ROOT->RPTR);
    }
}

void Postorder(struct node *ROOT)
{
    if (ROOT != NULL)
    {
        Preorder(ROOT->LPTR);
        Preorder(ROOT->RPTR);
        printf("%d,", ROOT->DATA);
    }
}

void main()
{
    int ch, n, value;
    printf("Enter Size of Tree:");
    scanf("%d", &n);

    for (int i = 0; i < n; i++)
    {
        int val;
        printf("Enter Value:");
        scanf("%d", &val);
        ROOT = create(ROOT, val);
    }

    do
    {
        printf(" 1)Insert\n 2)Preorder \n 3)Inorder \n 4)Postorder \n 5)Exit \n Enter your choice:");
        scanf("%d", &ch);
        switch (ch)
        {
        case 1:
            printf("Enter Value:");
            scanf("%d", &value);
            ROOT = create(ROOT, value);
            break;
        case 2:
            Preorder(ROOT);
            printf("\n");
            break;
        case 3:
            Inorder(ROOT);
            printf("\n");
            break;
        case 4:
            Postorder(ROOT);
            printf("\n");
            break;
        case 5:
            printf("Exit");
            break;
        default:
            printf("Invalid Choice:");
            break;
        }
    } while (ch != 5);
}