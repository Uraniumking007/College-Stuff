#include <stdio.h>
#define MAX_LENGTH 100
int stringLength(const char str[])
{
    int length = 0;
    while (str[length] != '\0')
    {
        length++;
    }
    return length;
}
void stringCopy(char dest[], const char src[])
{
    int i = 0;
    while (src[i] != '\0')
    {
        dest[i] = src[i];
        i++;
    }
    dest[i] = '\0';
}
void reverseString(char str[])
{
    int length = stringLength(str);
    for (int i = 0; i < length / 2; i++)
    {
        char temp = str[i];
        str[i] = str[length - 1 - i];
        str[length - 1 - i] = temp;
    }
}
void stringConcat(char dest[], const char src[])
{
    int dest_len = stringLength(dest);
    int i = 0;
    while (src[i] != '\0')
    {
        dest[dest_len + i] = src[i];
        i++;
    }
    dest[dest_len + i] = '\0';
}
int findSubstring(const char str[], const char substr[])
{
    int str_len = stringLength(str);
    int substr_len = stringLength(substr);

    for (int i = 0; i <= str_len - substr_len; i++)
    {
        int j;
        for (j = 0; j < substr_len; j++)
        {
            if (str[i + j] != substr[j])
            {
                break;
            }
        }
        if (j == substr_len)
        {
            return i;
        }
    }
    return -1;
}
int compareStrings(const char str1[], const char str2[])
{
    int i = 0;
    while (str1[i] != '\0' && str2[i] != '\0')
    {
        if (str1[i] < str2[i])
        {
            return -1;
        }
        else if (str1[i] > str2[i])
        {
            return 1;
        }
        i++;
    }
    if (str1[i] == '\0' && str2[i] == '\0')
    {
        return 0;
    }
    else
    {
        return -1;
    }
}
int main()
{
    char str1[MAX_LENGTH], str2[MAX_LENGTH];
    int choice;

    do
    {
        printf("\nString Operations Menu:\n");
        printf("1. Calculate string length\n");
        printf("2. Copy string\n");
        printf("3. Reverse string\n");
        printf("4. Concatenate strings\n");
        printf("5. Find substring\n");
        printf("6. Compare strings\n");
        printf("0. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);
        getchar();

        switch (choice)
        {
        case 1:
            printf("Enter a string: ");
            fgets(str1, MAX_LENGTH, stdin);
            str1[stringLength(str1) - 1] = '\0';
            printf("Length of the string: %d\n", stringLength(str1));
            break;
        case 2:
            printf("Enter a string: ");
            fgets(str1, MAX_LENGTH, stdin);
            str1[stringLength(str1) - 1] = '\0';
            stringCopy(str2, str1);
            printf("Copied string: %s\n", str2);
            break;
        case 3:
            printf("Enter a string: ");
            fgets(str1, MAX_LENGTH, stdin);
            str1[stringLength(str1) - 1] = '\0';
            reverseString(str1);
            printf("Reversed string: %s\n", str1);
            break;
        case 4:
            printf("Enter first string: ");
            fgets(str1, MAX_LENGTH, stdin);
            str1[stringLength(str1) - 1] = '\0';
            printf("Enter second string: ");
            fgets(str2, MAX_LENGTH, stdin);
            str2[stringLength(str2) - 1] = '\0';
            stringConcat(str1, str2);
            printf("Concatenated string: %s\n", str1);
            break;
        case 5:
            printf("Enter main string: ");
            fgets(str1, MAX_LENGTH, stdin);
            str1[stringLength(str1) - 1] = '\0';
            printf("Enter substring to find: ");
            fgets(str2, MAX_LENGTH, stdin);
            str2[stringLength(str2) - 1] = '\0';
            int index = findSubstring(str1, str2);
            if (index != -1)
            {
                printf("Substring found at index: %d\n", index);
            }
            else
            {
                printf("Substring not found\n");
            }
            break;
        case 6:
            printf("Enter first string: ");
            fgets(str1, MAX_LENGTH, stdin);
            str1[stringLength(str1) - 1] = '\0';
            printf("Enter second string: ");
            fgets(str2, MAX_LENGTH, stdin);
            str2[stringLength(str2) - 1] = '\0';
            int result = compareStrings(str1, str2);
            if (result == 0)
            {
                printf("Strings are equal\n");
            }
            else
            {
                printf("String are not equal\n");
            }
            break;
        case 0:
            printf("Exiting program.\n");
            break;
        default:
            printf("Invalid choice. Please try again.\n");
        }
    } while (choice != 0);

    return 0;
}
