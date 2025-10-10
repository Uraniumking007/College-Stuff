#include <stdio.h>

float calculate(float operand1, float operand2, char operator);

int main()
{
    float num1, num2, result;
    char operator;
    char choice;

    do
    {
        printf("Enter first number: ");
        scanf("%f", &num1);
        printf("Enter operator (+, -, *, /): ");
        scanf(" %c", &operator);

        printf("Enter second number: ");
        scanf("%f", &num2);

        result = calculate(num1, num2, operator);

        printf("Result: %.2f\n", result);

        printf("Do you want to perform another calculation? (y/n): ");
        scanf(" %c", &choice);

    } while (choice == 'y' || choice == 'Y');

    printf("Thank you for using the calculator!\n");

    return 0;
}

float calculate(float operand1, float operand2, char operator)
{
    float result;

    switch (operator)
    {
    case '+':
        result = operand1 + operand2;
        break;
    case '-':
        result = operand1 - operand2;
        break;
    case '*':
        result = operand1 * operand2;
        break;
    case '/':
        if (operand2 != 0)
        {
            result = operand1 / operand2;
        }
        else
        {
            printf("Error: Division by zero!\n");
            result = 0;
        }
        break;
    default:
        printf("Error: Invalid operator!\n");
        result = 0;
    }

    return result;
}