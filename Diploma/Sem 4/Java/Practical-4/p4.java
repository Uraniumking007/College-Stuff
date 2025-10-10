import java.io.*;
import java.util.Scanner;

class Switching {
    public static int a, b, calc;

    public static void main(String[] args) {
        switch (args[0]) {
            case "1":
                min();
                break;
            case "2":
                add();
                break;
            case "3":
                Multiplication();
                break;

            default:
                System.out.println("Invalid Selection");
                break;
        }
    }

    public static void min() {
        Scanner input = new Scanner(System.in);
        System.out.println("Enter First Number: ");
        a = input.nextInt();
        System.out.println("Enter Second Number: ");
        b = input.nextInt();
        if (a < b) {
            System.out.println(a + " is Min");
        } else {
            System.out.println(b + "is Min");
        }
    }

    public static void add() {
        Scanner input = new Scanner(System.in);
        System.out.println("Enter First Number: ");
        a = input.nextInt();
        System.out.println("Enter Second Number: ");
        b = input.nextInt();
        calc = a + b;
        System.out.println("Addition: " + calc);
    }

    public static void Multiplication() {
        Scanner input = new Scanner(System.in);
        System.out.println("Enter First Number: ");
        a = input.nextInt();
        System.out.println("Enter Second Number: ");
        b = input.nextInt();
        calc = a * b;
        System.out.println("Multiplication: " + calc);
    }
}