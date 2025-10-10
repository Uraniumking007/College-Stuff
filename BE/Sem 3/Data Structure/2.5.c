// Stack ops
/*
Push
Pop
Peep
Change
Display
*/

#include <stdio.h>

int S[10];
int top = -1;
int N = 5;

void push()
{
    int X;
    if (top >= N - 1)
    {
        printf("Stack Overflow\n");
    }
    else
    {
        top++;
        printf("Enter Element:");
        scanf("%d", &X);
        S[top] = X;
    }
}

void Display()
{
    for (int i = 0; i <= top; i++)
    {
        printf("%d :- %d\n", i, S[i]);
    }
}

int pop()
{
    if (top == -1)
    {
        printf("Stack Underflow\n");
        return -1;
    }

    top -= 1;
    return S[top + 1];
}

int peep()
{
    if (top == -1)
    {
        printf("Stack Underflow\n");
        return -1;
    }
    else
        return S[top];
}

void change()
{
    pop();
    push();
}

void main()
{
    int ch, V, P, m = 1;

    while (m != 0)
    {
        printf("Enter your Choice:- \n 1)Push \n 2)Display \n 3)Pop \n 4)Peep \n5)Change \n");
        scanf("%d", &ch);
        switch (ch)
        {
        case 1:
            push();
            break;

        case 2:
            Display();
            break;

        case 3:
            V = pop();
            printf("Poped Element is %d\n", V);
            break;

        case 4:
            P = peep();
            printf("Top most Element is %d\n", P);
            break;
        case 5:
            change();
            break;

        default:
            printf("Invalid Choice\n");
            break;
        }
        printf("Enter 0 to stop and press any number to continue\n");
        scanf("%d", &m);
    }
}