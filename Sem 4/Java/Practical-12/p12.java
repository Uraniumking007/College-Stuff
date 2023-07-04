// Practical 12-A
class Student {
    int enrollmentNo;
    int examNo;
    String studentName;

    Student(int a, int b, String c) {
        enrollmentNo = a;
        examNo = b;
        studentName = c;
    }
}

class Exam extends Student {
    int marks1;
    int marks2;
    int marks3;

    Exam(int a, int b, String c, int d, int e, int f) {
        super(a, b, c);
        marks1 = d;
        marks2 = e;
        marks3 = f;
    }
}

class Result extends Exam {
    int totalMarks;
    float percentage;

    Result(int enrollmentNo, int examNo, String studentName, int marks1, int marks2, int marks3) {
        super(enrollmentNo, examNo, studentName, marks1, marks2, marks3);
        totalMarks = marks1 + marks2 + marks3;
        percentage = (float) totalMarks / 3;
    }

    public static void main(String[] args) {
        Result r = new Result(046, 9, "Bhavesh", 95, 89, 85);

        System.out.println("Name: " + r.studentName);
        System.out.println("Enrollment No: " + r.enrollmentNo);
        System.out.println("Exam No: " + r.examNo);
        System.out.println("Marks 1: " + r.marks1);
        System.out.println("Marks 2: " + r.marks2);
        System.out.println("Marks 3: " + r.marks3);
        System.out.println("Total marks: " + r.totalMarks);
        System.out.println("Percentage: " + r.percentage);

    }
}

// Practical 12-B
class GrandFather {
    String surname;
    String nationality;

    public GrandFather(String a, String b) {
        surname = a;
        nationality = b;
    }
}

class Father extends GrandFather {
    String name;

    public Father(String a, String b, String c) {
        super(b, c);
        name = a;
    }
}

class Son extends GrandFather {
    String name;

    public Son(String a, String b, String c) {
        super(b, c);
        name = a;
    }
}

class p12b {
    public static void main(String[] args) {
        GrandFather grandFather = new GrandFather("Escobar", "American");
        Father father = new Father("John", "Doe", "American");
        Son son = new Son("Garra", "Doe", "American");

        System.out.println("Grandfather Details:");
        System.out.println("Surname: " + grandFather.surname);
        System.out.println("Nationality: " + grandFather.nationality);

        System.out.println("\nFather Details:");
        System.out.println("Name: " + father.name);
        System.out.println("Surname: " + father.surname);
        System.out.println("Nationality: " + father.nationality);

        System.out.println("\nSon Details:");
        System.out.println("Name: " + son.name);
        System.out.println("Surname: " + son.surname);
        System.out.println("Nationality: " + son.nationality);
    }
}
