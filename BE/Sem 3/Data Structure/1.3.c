#include <stdio.h>

#define MAX_ROWS 10
#define MAX_COLS 10

// Function to input a matrix
void inputMatrix(int matrix[MAX_ROWS][MAX_COLS], int rows, int cols)
{
    printf("Enter the elements of the matrix (%dx%d):\n", rows, cols);
    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < cols; j++)
        {
            scanf("%d", &matrix[i][j]);
        }
    }
}

// Function to display a matrix
void displayMatrix(int matrix[MAX_ROWS][MAX_COLS], int rows, int cols)
{
    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < cols; j++)
        {
            printf("%d\t", matrix[i][j]);
        }
        printf("\n");
    }
}

// Function to add two matrices
void addMatrices(int matrix1[MAX_ROWS][MAX_COLS], int matrix2[MAX_ROWS][MAX_COLS],
                 int result[MAX_ROWS][MAX_COLS], int rows, int cols)
{
    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < cols; j++)
        {
            result[i][j] = matrix1[i][j] + matrix2[i][j];
        }
    }
}

// Function to subtract two matrices
void subtractMatrices(int matrix1[MAX_ROWS][MAX_COLS], int matrix2[MAX_ROWS][MAX_COLS],
                      int result[MAX_ROWS][MAX_COLS], int rows, int cols)
{
    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < cols; j++)
        {
            result[i][j] = matrix1[i][j] - matrix2[i][j];
        }
    }
}

// Function to multiply two matrices
void multiplyMatrices(int matrix1[MAX_ROWS][MAX_COLS], int matrix2[MAX_ROWS][MAX_COLS],
                      int result[MAX_ROWS][MAX_COLS], int rows1, int cols1, int cols2)
{
    for (int i = 0; i < rows1; i++)
    {
        for (int j = 0; j < cols2; j++)
        {
            result[i][j] = 0;
            for (int k = 0; k < cols1; k++)
            {
                result[i][j] += matrix1[i][k] * matrix2[k][j];
            }
        }
    }
}

int main()
{
    int matrix1[MAX_ROWS][MAX_COLS], matrix2[MAX_ROWS][MAX_COLS], result[MAX_ROWS][MAX_COLS];
    int rows1, cols1, rows2, cols2;
    int choice;

    do
    {
        printf("\nMatrix Operations Menu:\n");
        printf("1. Addition\n");
        printf("2. Subtraction\n");
        printf("3. Multiplication\n");
        printf("0. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice)
        {
        case 1: // Addition
        case 2: // Subtraction
            printf("Enter dimensions of matrices (rows columns): ");
            scanf("%d %d", &rows1, &cols1);
            rows2 = rows1;
            cols2 = cols1;

            printf("For first matrix:\n");
            inputMatrix(matrix1, rows1, cols1);
            printf("For second matrix:\n");
            inputMatrix(matrix2, rows2, cols2);

            if (choice == 1)
            {
                addMatrices(matrix1, matrix2, result, rows1, cols1);
                printf("Result of addition:\n");
            }
            else
            {
                subtractMatrices(matrix1, matrix2, result, rows1, cols1);
                printf("Result of subtraction:\n");
            }
            displayMatrix(result, rows1, cols1);
            break;

        case 3: // Multiplication
            printf("Enter dimensions of first matrix (rows columns): ");
            scanf("%d %d", &rows1, &cols1);
            printf("Enter dimensions of second matrix (rows columns): ");
            scanf("%d %d", &rows2, &cols2);

            if (cols1 != rows2)
            {
                printf("Error: Number of columns in first matrix must equal number of rows in second matrix.\n");
                break;
            }

            printf("For first matrix:\n");
            inputMatrix(matrix1, rows1, cols1);
            printf("For second matrix:\n");
            inputMatrix(matrix2, rows2, cols2);

            multiplyMatrices(matrix1, matrix2, result, rows1, cols1, cols2);
            printf("Result of multiplication:\n");
            displayMatrix(result, rows1, cols2);
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