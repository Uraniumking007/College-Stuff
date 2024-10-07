#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>

int S[10];
int top = -1;
int N = 5;

void push(char X)
{
    if (top >= N - 1)
    {
        printf("Stack Overflow\n");
    }
    else
    {
        top++;
        S[top] = X;
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

int atoint(char str)
{
    switch (str)
    {
    case '1':
        return 1;
        break;
    case '2':
        return 2;
        break;
    case '3':
        return 3;
        break;
    case '4':
        return 4;
        break;
    case '5':
        return 5;
        break;
    case '6':
        return 6;
        break;
    case '7':
        return 7;
        break;
    case '8':
        return 8;
        break;
    case '9':
        return 9;
        break;
    case '0':
        return 0;
        break;

    default:
        break;
    }
}

void postfixEval(char *strr)
{
    int i = 0;
    while (strr[i] != '\0')
    {
        if (isdigit(strr[i]))
        {
            push(atoint(strr[i]));
        }
        else
        {
            int b = pop();
            int a = pop();

            switch (strr[i])
            {
            case '+':
                push(a + b);
                break;
            case '-':
                push(a - b);
                break;
            case '/':
                push(a / b);
                break;
            case '*':
                push(a * b);
                break;

            default:
                break;
            }
        }
        i++;
    }

    // 12+56+-
    printf("Evaluation of provided postfix equation: %d ", S[0]);
}

void main()
{
    int ch, V, P, m = 1;
    char str[100];

    printf("Enter Postfix Equation to be Evaluate.");
    gets(str);

    postfixEval(str);
}