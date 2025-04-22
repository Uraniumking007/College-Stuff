public class LCMCalculator {
    public static void main(String[] args) {
        findLCM(12, 18);
        findLCM(5, 7);
        findLCM(24, 36);
    }
    
    public static void findLCM(int num1, int num2) {
        int lcm = calculateLCM(num1, num2);
        System.out.println("LCM of " + num1 + " and " + num2 + " is: " + lcm);
    }
    
    public static int calculateLCM(int num1, int num2) {
        int gcd = findGCD(num1, num2);
        return (num1 * num2) / gcd;
    }
    
    public static int findGCD(int num1, int num2) {
        while (num2 != 0) {
            int temp = num2;
            num2 = num1 % num2;
            num1 = temp;
        }
        return num1;
    }
}
