import java.util.Scanner;

public class p3 {

    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.println("Enter Value in Meter: ");
        double a = input.nextDouble();

        System.out.println("Value in Feet is " + a * 3.28084);

    }
}
