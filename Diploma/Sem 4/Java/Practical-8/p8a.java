import java.util.*;

class Student {
    int student_id, student_marks, subject_code;

    void getData(int a, int b, int c) {
        student_id = a;
        subject_code = b;
        student_marks = c;
    }

    void putData() {
        System.out.println("Student Id: " + student_id);
        System.out.println("Subject Code: " + subject_code);
        System.out.println("Student Marks: " + student_marks);
    }
}

public class p8a {
    public static void main(String[] args) {
        int a, b, c;
        Student s1 = new Student();
        Scanner input = new Scanner(System.in);
        System.out.println("Enter Student ID: ");
        a = input.nextInt();
        System.out.println("Enter Subject Code: ");
        b = input.nextInt();
        System.out.println("Enter Student Marks: ");
        c = input.nextInt();
        s1.getData(a, b, c);
        s1.putData();
    }
}