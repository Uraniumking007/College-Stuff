#include <stdio.h>
#include <math.h>

int binaryToDecimal(int n)
{
    int decimalNumber = 0;
    int i = 0;
    int remainder;

    while (n != 0)
    {
        remainder = n % 10;
        n /= 10;
        decimalNumber += remainder * pow(2, i);
        ++i;
    }
    return decimalNumber;
}

long long decimalToBinary(int n)
{
    long long binaryNumber = 0;
    int remainder, i = 1;
    while (n != 0)
    {
        remainder = n % 2;
        n /= 2;
        binaryNumber += remainder * i;
        i *= 10;
    }
    return binaryNumber;
}

int main()
{
    int choice, number;
    printf("Choose the conversion type:\n");
    printf("1. Binary to Decimal\n");
    printf("2. Decimal to Binary\n");
    printf("Enter your choice: ");
    scanf("%d", &choice);

    switch (choice)
    {
    case 1:
        printf("Enter a binary number: ");
        scanf("%d", &number);
        printf("Decimal equivalent: %d\n", binaryToDecimal(number));
        break;
    case 2:
        printf("Enter a decimal number: ");
        scanf("%d", &number);
        printf("Binary equivalent: %lld\n", decimalToBinary(number));
        break;
    default:
        printf("Invalid choice!\n");
    }

    return 0;
}