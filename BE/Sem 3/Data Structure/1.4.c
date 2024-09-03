#include <stdio.h>
#include <string.h>

#define MAX_EMPLOYEES 5
#define MAX_NAME_LENGTH 50
#define MAX_DESIGNATION_LENGTH 50
#define MAX_DEPARTMENT_LENGTH 50

struct Employee
{
    int emp_id;
    char emp_name[MAX_NAME_LENGTH];
    char emp_designation[MAX_DESIGNATION_LENGTH];
    float emp_salary;
    char emp_department[MAX_DEPARTMENT_LENGTH];
};

void inputEmployee(struct Employee *emp)
{
    printf("Enter Employee ID: ");
    scanf("%d", &emp->emp_id);
    getchar(); // Consume newline

    printf("Enter Employee Name: ");
    fgets(emp->emp_name, MAX_NAME_LENGTH, stdin);
    emp->emp_name[strcspn(emp->emp_name, "\n")] = 0;

    printf("Enter Employee Designation: ");
    fgets(emp->emp_designation, MAX_DESIGNATION_LENGTH, stdin);
    emp->emp_designation[strcspn(emp->emp_designation, "\n")] = 0;

    printf("Enter Employee Salary: ");
    scanf("%f", &emp->emp_salary);
    getchar(); // Consume newline

    printf("Enter Employee Department: ");
    fgets(emp->emp_department, MAX_DEPARTMENT_LENGTH, stdin);
    emp->emp_department[strcspn(emp->emp_department, "\n")] = 0;
}

void displayEmployee(const struct Employee *emp)
{
    printf("ID: %d, Name: %s, Designation: %s, Salary: %.2f, Department: %s\n",
           emp->emp_id, emp->emp_name, emp->emp_designation, emp->emp_salary, emp->emp_department);
}

float findHighestSalary(const struct Employee employees[], int count)
{
    float highest = employees[0].emp_salary;
    for (int i = 1; i < count; i++)
    {
        if (employees[i].emp_salary > highest)
        {
            highest = employees[i].emp_salary;
        }
    }
    return highest;
}

int countEmployeesInDepartment(const struct Employee employees[], int count, const char *department)
{
    int departmentCount = 0;
    for (int i = 0; i < count; i++)
    {
        if (strcmp(employees[i].emp_department, department) == 0)
        {
            departmentCount++;
        }
    }
    return departmentCount;
}

void displayAllRecords(const struct Employee employees[], int count)
{
    printf("All Employee Records:\n");
    for (int i = 0; i < count; i++)
    {
        displayEmployee(&employees[i]);
    }
}

int main()
{
    struct Employee employees[MAX_EMPLOYEES];
    int employeeCount = 0;
    int choice;
    char department[MAX_DEPARTMENT_LENGTH];

    printf("Enter information for %d employees:\n", MAX_EMPLOYEES);
    for (int i = 0; i < MAX_EMPLOYEES; i++)
    {
        printf("\nEmployee %d:\n", i + 1);
        inputEmployee(&employees[i]);
        employeeCount++;
    }

    do
    {
        printf("\nEmployee Management Menu:\n");
        printf("1. Find Highest Salary\n");
        printf("2. Count Employees in Department\n");
        printf("3. Display All Records\n");
        printf("0. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);
        getchar();

        switch (choice)
        {
        case 1:
            printf("Highest salary among all employees: %.2f\n", findHighestSalary(employees, employeeCount));
            break;
        case 2:
            printf("Enter department name: ");
            fgets(department, MAX_DEPARTMENT_LENGTH, stdin);
            department[strcspn(department, "\n")] = 0;
            printf("Number of employees in %s department: %d\n",
                   department, countEmployeesInDepartment(employees, employeeCount, department));
            break;
        case 3:
            displayAllRecords(employees, employeeCount);
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