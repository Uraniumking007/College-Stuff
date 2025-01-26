import java.util.Scanner;
import java.util.*;

public class sorting {

    static int takeValue(String inputText) {
        Scanner sc = new Scanner(System.in);
        System.out.println(inputText);

        return sc.nextInt();
    }

    public static void main(String[] args) {
        int a = takeValue("Enter A");
        int b = takeValue("Enter B");
        int c = takeValue("Enter C");
        int[] arr = { a, b, c };

        for (int i = 0; i < arr.length - 1; i++) {
            for (int j = 0; j < arr.length - 1 - i; j++) {
                if (arr[j] < arr[j + 1]) {
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                }
            }
        }

        System.out.println("Sorted Data: " + Arrays.toString(arr));

    }

}
