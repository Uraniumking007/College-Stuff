import java.util.*;

class posorneg {
    public static void main(String[] args) {
        int a = 10;
        if (a > 0) {
            System.out.println(a + " is Positive");
        } else if (a < 0) {
            System.out.println(a + " is Negative");
        } else {
            System.out.println(a + " is Zero");

        }
    }
}

class divby3 {
    public static void main(String[] args) {
        int a = 20;
        if (a % 3 == 0) {
            System.out.println(a + " is Divisible by 3");
        } else {
            System.out.println(a + " is not Divisible by 3");
        }
    }
}

class Leap {
    public static void main(String[] args) {
        int y = 1992;
        if (y % 4 == 0) {
            System.out.println(y + " is a Leap year");
        } else {
            System.out.println(y + " is a not Leap year");
        }
    }
}

class OldCalc {
    public static void main(String[] args) {
        int a, b, c, d;
        Scanner sc = new Scanner(System.in);
        System.out.println("Age of First Person");
        a = sc.nextInt();
        System.out.println("Age of Second Person");
        b = sc.nextInt();
        System.out.println("Age of Second Person");
        c = sc.nextInt();

        if (a > b) {
            if (a > c) {
                System.out.println("First person is oldest");
            }
        } else {
            if (b > c) {
                System.out.println("Second Person is Oldest");
            } else {
                System.out.println("Third person is Oldest");
            }
        }
    }
}
