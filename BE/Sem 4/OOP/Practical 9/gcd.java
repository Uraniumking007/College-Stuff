import java.util.Scanner;

public class gcd {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);

        System.out.print("Enter first integer: ");
        int num1 = input.nextInt();
        System.out.print("Enter second integer: ");
        int num2 = input.nextInt();

        System.out.println("The GCD of " + num1 + " and " + num2 + " is " + calcGCD(num1, num2));

    }

    public static int calcGCD(int num1, int num2) {
        num1 = Math.abs(num1);
        num2 = Math.abs(num2);

        while (num2 != 0) {
            int temp = num2;
            num2 = num1 % num2;
            num1 = temp;
        }

        return num1;
    }
}