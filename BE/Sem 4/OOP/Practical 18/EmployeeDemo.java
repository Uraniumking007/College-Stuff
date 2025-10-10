class Employee {
    private int employee_Id;
    private String employee_Name;

    public Employee() {
        this.employee_Id = 0;
        this.employee_Name = "";
    }

    public Employee(int employee_Id, String employee_Name) {
        this.employee_Id = employee_Id;
        this.employee_Name = employee_Name;
    }

    public void insertDetails(int employee_Id, String employee_Name) {
        this.employee_Id = employee_Id;
        this.employee_Name = employee_Name;
    }

    public void updateDetails(int employee_Id, String employee_Name) {
        this.employee_Id = employee_Id;
        this.employee_Name = employee_Name;
    }

    public void displayDetails() {
        System.out.println("Employee ID: " + employee_Id);
        System.out.println("Employee Name: " + employee_Name);
    }

    public int getEmployee_Id() {
        return employee_Id;
    }

    public void setEmployee_Id(int employee_Id) {
        this.employee_Id = employee_Id;
    }

    public String getEmployee_Name() {
        return employee_Name;
    }

    public void setEmployee_Name(String employee_Name) {
        this.employee_Name = employee_Name;
    }
}

class SalariedEmployee extends Employee {
    private String designation;
    private double monthly_salary;

    public SalariedEmployee() {
        super();
        this.designation = "";
        this.monthly_salary = 0.0;
    }

    public SalariedEmployee(int employee_Id, String employee_Name, String designation, double monthly_salary) {
        super(employee_Id, employee_Name);
        this.designation = designation;
        this.monthly_salary = monthly_salary;
    }

    public void insertDetails(int employee_Id, String employee_Name, String designation, double monthly_salary) {
        super.insertDetails(employee_Id, employee_Name);
        this.designation = designation;
        this.monthly_salary = monthly_salary;
    }

    public void updateDetails(int employee_Id, String employee_Name, String designation, double monthly_salary) {
        super.updateDetails(employee_Id, employee_Name);
        this.designation = designation;
        this.monthly_salary = monthly_salary;
    }

    @Override
    public void displayDetails() {
        super.displayDetails();
        System.out.println("Designation: " + designation);
        System.out.println("Monthly Salary: $" + monthly_salary);
    }

    public String getDesignation() {
        return designation;
    }

    public void setDesignation(String designation) {
        this.designation = designation;
    }

    public double getMonthly_salary() {
        return monthly_salary;
    }

    public void setMonthly_salary(double monthly_salary) {
        this.monthly_salary = monthly_salary;
    }
}

public class EmployeeDemo {
    public static void main(String[] args) {
        System.out.println("EMPLOYEE CLASS DEMONSTRATION");
        System.out.println("---------------------------");

        Employee emp1 = new Employee();
        emp1.insertDetails(101, "John Doe");
        System.out.println("Employee 1 details after insertion:");
        emp1.displayDetails();

        Employee emp2 = new Employee(102, "Jane Smith");
        System.out.println("\nEmployee 2 details:");
        emp2.displayDetails();

        emp2.updateDetails(102, "Jane Wilson");
        System.out.println("\nEmployee 2 details after update:");
        emp2.displayDetails();

        System.out.println("\nSALARIED EMPLOYEE DEMONSTRATION");
        System.out.println("------------------------------");

        SalariedEmployee semp1 = new SalariedEmployee();
        semp1.insertDetails(201, "Robert Johnson", "Software Developer", 5000.0);
        System.out.println("Salaried Employee 1 details after insertion:");
        semp1.displayDetails();

        SalariedEmployee semp2 = new SalariedEmployee(202, "Mary Williams", "Project Manager", 8000.0);
        System.out.println("\nSalaried Employee 2 details:");
        semp2.displayDetails();

        semp2.updateDetails(202, "Mary Williams", "Senior Project Manager", 9500.0);
        System.out.println("\nSalaried Employee 2 details after update:");
        semp2.displayDetails();
    }
}
