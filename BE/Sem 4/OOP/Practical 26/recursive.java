import java.util.Scanner;

public class recursive {
    public static int findMinimum(int[] array, int length) {
        if (length == 1) {
            return array[0];
        }
        
        int minInSubArray = findMinimum(array, length - 1);
        
        return Math.min(minInSubArray, array[length - 1]);
    }
    
    public static long calculateProduct(int n) {
        long product = 1;
        for (int i = 1; i <= n; i++) {
            product *= i;
        }
        return product;
    }
    
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        
        System.out.print("Enter the number of elements in the array: ");
        int size = input.nextInt();
        int[] numbers = new int[size];
        
        System.out.println("Enter " + size + " integers:");
        for (int i = 0; i < size; i++) {
            numbers[i] = input.nextInt();
        }
        
        int smallest = findMinimum(numbers, numbers.length);
        System.out.println("The smallest integer in the array is: " + smallest);
        
        System.out.print("\nEnter an integer to calculate its product: ");
        int n = input.nextInt();
        long product = calculateProduct(n);
        System.out.println("Product of numbers from 1 to " + n + " is: " + product);
        
        input.close();
    }
}