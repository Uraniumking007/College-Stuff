/**
 * Demo class to test the Employee and SalariedEmployee classes
 */
public class EmployeeDemo {
    public static void main(String[] args) {
        // Testing Employee class
        System.out.println("TESTING EMPLOYEE CLASS");
        System.out.println("----------------------");
        
        // Create employee using default constructor and insert details
        Employee emp1 = new Employee();
        emp1.insertDetails(101, "John Doe");
        System.out.println("Employee 1 details after insertion:");
        emp1.displayDetails();
        
        // Create employee using parameterized constructor
        Employee emp2 = new Employee(102, "Jane Smith");
        System.out.println("\nEmployee 2 details:");
        emp2.displayDetails();
        
        // Update employee details
        emp2.updateDetails(102, "Jane Wilson");
        System.out.println("\nEmployee 2 details after update:");
        emp2.displayDetails();
        
        // Testing SalariedEmployee class
        System.out.println("\n\nTESTING SALARIED EMPLOYEE CLASS");
        System.out.println("-------------------------------");
        
        // Create salaried employee using default constructor and insert details
        SalariedEmployee semp1 = new SalariedEmployee();
        semp1.insertDetails(201, "Robert Johnson", "Software Developer", 5000.0);
        System.out.println("Salaried Employee 1 details after insertion:");
        semp1.displayDetails();
        
        // Create salaried employee using parameterized constructor
        SalariedEmployee semp2 = new SalariedEmployee(202, "Mary Williams", "Project Manager", 8000.0);
        System.out.println("\nSalaried Employee 2 details:");
        semp2.displayDetails();
        
        // Update salaried employee details
        semp2.updateDetails(202, "Mary Williams", "Senior Project Manager", 9500.0);
        System.out.println("\nSalaried Employee 2 details after update:");
        semp2.displayDetails();
    }
}
