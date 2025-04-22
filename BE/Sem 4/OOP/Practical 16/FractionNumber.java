import java.util.Scanner;

public class FractionNumber {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        
        System.out.print("Enter a decimal number: ");
        String decimal = input.nextLine();
        
        int indexOfDecimalPoint = decimal.indexOf('.');
        
        if (indexOfDecimalPoint < 0) {
            System.out.println(decimal + "/1");
            input.close();
            return;
        }
        
        String integerPart = decimal.substring(0, indexOfDecimalPoint);
        String fractionalPart = decimal.substring(indexOfDecimalPoint + 1);
        
        long numerator = Long.parseLong(integerPart + fractionalPart);
        long denominator = (long)Math.pow(10, fractionalPart.length());
        
        if (decimal.charAt(0) == '-') {
            numerator = -numerator;
        }
        
        long gcd = gcd(Math.abs(numerator), denominator);
        
        numerator /= gcd;
        denominator /= gcd;
        
        System.out.println("The fraction number is " + numerator + "/" + denominator);
        
        input.close();
    }
    
    private static long gcd(long a, long b) {
        while (b != 0) {
            long temp = b;
            b = a % b;
            a = temp;
        }
        return a;
    }
}