#include <stdio.h>
#include <ctype.h>

#define MAX 100

struct Stack
{
    int top;
    char items[MAX];
};

void push(struct Stack *s, char item)
{
    if (s->top == (MAX - 1))
    {
        printf("Stack Overflow\n");
        return;
    }
    s->items[++(s->top)] = item;
}

char pop(struct Stack *s)
{
    if (s->top == -1)
    {
        printf("Stack Underflow\n");
        return '\0';
    }
    return s->items[(s->top)--];
}

char peek(struct Stack *s)
{
    if (s->top == -1)
    {
        return '\0';
    }
    return s->items[s->top];
}

int precedence(char op)
{
    switch (op)
    {
    case '+':
    case '-':
        return 1;
    case '*':
    case '/':
        return 2;
    case '^':
        return 3;
    default:
        return 0;
    }
}

int isOperator(char ch)
{
    return ch == '+' || ch == '-' || ch == '*' || ch == '/' || ch == '^';
}

void infixToPostfix(char *infix, char *postfix)
{
    struct Stack s;
    s.top = -1;
    int i = 0, j = 0;
    char ch;

    while ((ch = infix[i++]) != '\0')
    {
        if (isalnum(ch))
        {
            postfix[j++] = ch;
        }
        else if (ch == '(')
        {
            push(&s, ch);
        }
        else if (ch == ')')
        {
            while (s.top != -1 && peek(&s) != '(')
            {
                postfix[j++] = pop(&s);
            }
            pop(&s); // Remove '(' from stack
        }
        else if (isOperator(ch))
        {
            while (s.top != -1 && precedence(peek(&s)) >= precedence(ch))
            {
                postfix[j++] = pop(&s);
            }
            push(&s, ch);
        }
    }

    while (s.top != -1)
    {
        postfix[j++] = pop(&s);
    }

    postfix[j] = '\0';
}

int main()
{
    char infix[MAX], postfix[MAX];

    printf("Enter infix expression: ");
    gets(infix);

    infixToPostfix(infix, postfix);

    printf("Postfix expression: %s\n", postfix);

    return 0;
}