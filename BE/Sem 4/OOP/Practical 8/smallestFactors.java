import java.util.Scanner;

public class smallestFactors {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        
        System.out.print("Enter an integer: ");
        int number = input.nextInt();
        
        System.out.print("The smallest factors of " + number + " are: ");
        
        int divisor = 2;
        while (number > 1) {
            if (number % divisor == 0) {
                System.out.print(divisor);
                number = number / divisor;
                if (number > 1) {
                    System.out.print(", ");
                }
            } else {
                divisor++;
            }
        }
   }
}