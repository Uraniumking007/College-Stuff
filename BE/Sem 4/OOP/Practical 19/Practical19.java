public class Practical19 {
    public static void main(String[] args) {
        IT_dept itDepartment = new IT_dept("CKPCET", "Surat", "Dr. Ami Choksi", 71);

        System.out.println("IT DEPARTMENT DETAILS");
        System.out.println("=====================");

        itDepartment.display();

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
        System.out.println("1. Discrete Mathematics");
        System.out.println("2. Object-Oriented Programming");
        System.out.println("3. Computer Architecture and Organization");
        System.out.println("4. Operating Systems and Virtualization");
        System.out.println("5. Principles of Economics");
    }
}
