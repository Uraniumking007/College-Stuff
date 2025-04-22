public class Practical19 {
    public static void main(String[] args) {
        // Create an instance of IT_dept
        IT_dept itDepartment = new IT_dept("XYZ University", "Mumbai", "Dr. Sharma", 250);

        System.out.println("IT DEPARTMENT DETAILS");
        System.out.println("=====================");

        // Display department details
        itDepartment.display();

        // Display subject list
        itDepartment.subject_list();
    }
}

abstract class Department {
    protected String university;
    protected String city;

    public Department(String university, String city) {
        this.university = university;
        this.city = city;
    }

    public void display() {
        System.out.println("University: " + university);
        System.out.println("City: " + city);
    }

    public abstract void subject_list();
}

class IT_dept extends Department {
    private String departmentHead;
    private int totalStudents;

    public IT_dept(String university, String city, String departmentHead, int totalStudents) {
        super(university, city);
        this.departmentHead = departmentHead;
        this.totalStudents = totalStudents;
    }

    @Override
    public void display() {
        System.out.println("Department: Information Technology");
        super.display();
        System.out.println("Department Head: " + departmentHead);
        System.out.println("Total Students: " + totalStudents);
    }

    @Override
    public void subject_list() {
        System.out.println("\nSubjects offered by IT Department:");
        System.out.println("1. Data Structures and Algorithms");
        System.out.println("2. Object-Oriented Programming");
        System.out.println("3. Database Management Systems");
        System.out.println("4. Computer Networks");
        System.out.println("5. Web Development");
        System.out.println("6. Artificial Intelligence");
    }
}
