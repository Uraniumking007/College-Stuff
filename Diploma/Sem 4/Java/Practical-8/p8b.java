import java.util.*;

class Person {
    String person_id, person_name, age_group;
    int person_age;

    void getData(String a, String b, int c) {
        person_id = a;
        person_name = b;
        person_age = c;
    }

    String ageGroup(int d) {
        if (d < 8) {
            age_group = "Child";
        } else if (d >= 8 && d < 20) {
            age_group = "Teenage";
        } else if (d >= 20 && d <= 40) {
            age_group = "Young";
        } else {
            age_group = "Old";
        }
        return age_group;
    }

    void putData() {
        System.out.println("Person ID: " + person_id);
        System.out.println("Name: " + person_name);
        System.out.println("Age: " + person_age);
        ageGroup(person_age);
        System.out.println("Age Group: " + age_group);
    }
}

public class p8b {
    public static void main(String[] args) {
        String a, b;
        int c;
        Person p1 = new Person();
        Scanner input = new Scanner(System.in);
        System.out.println("Enter Person ID: ");
        a = input.nextLine();
        System.out.println("Enter Person Name: ");
        b = input.nextLine();
        System.out.println("Enter Person Age: ");
        c = input.nextInt();
        p1.getData(a, b, c);
        p1.putData();
    }
}
