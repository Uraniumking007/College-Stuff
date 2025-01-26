import java.util.Scanner;

public class p4 {
    Scanner sc = new Scanner(System.in);

    static double takeValue(String inputText) {
        Scanner sc = new Scanner(System.in);
        System.out.println(inputText);

        return sc.nextDouble();
    }

    static double calculateBMI(double w, double h) {
        return (w * 0.45359237) / ((h * 0.254) * (h * 0.254)) * 100;
    }

    public static void main(String[] args) {

        System.out.println("BMI Calculator");

        double weight = takeValue("Enter Weight in Pound (lbs): ");
        double height = takeValue("Enter Height in Inches:");

        double bmi = calculateBMI(weight, height);

        System.out.println("BMI on basis of provided value is " + bmi);

    }
}
