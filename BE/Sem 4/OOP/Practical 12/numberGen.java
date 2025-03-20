//Write a program that creates a Random object with seed 1000 and displays the first 100random integers between 1 and 49 using the NextInt (49) method.

import java.util.Random;

public class numberGen {

    public static void main(String[] args) {
        Random rand = new Random(1000);
        int[] numbers = new int[100];

        for (int i = 0; i < 100; i++) {
            int x = rand.nextInt(49);
            numbers[i] = x;
        }

        System.out.println("First 100 random integers between 1 and 49 are: ");
        System.out.print("[");
        for (int i = 0; i < 100; i++) {
            System.out.print(numbers[i] + (i == 99 ? "" : ", "));
        }
        System.out.print("]");

    }

}
