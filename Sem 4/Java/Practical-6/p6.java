import java.lang.reflect.Array;
import java.util.*;

class copyArray {
    public static void main(String[] args) {
        int[] arr1 = { 25, 35, 65 };
        int[] arr2 = new int[3];
        System.out.println("Array 1:");

        for (int i = 0; i < arr1.length; i++) {
            System.out.println(arr1[i]);
        }
        for (int i = 0; i < arr1.length; i++) {
            arr2[i] = arr1[i];
        }
        System.out.println("Array 2:");

        for (int i = 0; i < arr2.length; i++) {
            System.out.println(arr2[i]);
        }
    }
}

class EvenInArray {
    public static void main(String[] args) {
        int count = 0;
        int[] arr1 = { 25, 24, 22, 26, 35, 33, 32 };
        for (int i = 0; i < arr1.length; i++) {
            if (arr1[i] % 2 == 0) {
                count++;
            }
        }
        System.out.println("No. of Even No: " + count);
    }
}

class SortArrayAsc {
    public static void main(String[] args) {
        int[] arr1 = { 226, 12, 14, 100, 32 };
        System.out.println("Original Array");
        for (int i = 0; i < arr1.length; i++) {
            System.out.println(arr1[i]);
        }
        Arrays.sort(arr1);
        System.out.println("Sorted Array");
        for (int i = 0; i < arr1.length; i++) {
            System.out.println(arr1[i]);
        }
    }
}

class SortArrayAscLogic {
    public static void main(String[] args) {
        int temp;
        int[] arr1 = { 226, 12, 14, 100, 32 };
        System.out.println("Original Array");
        for (int i = 0; i < arr1.length; i++) {
            System.out.println(arr1[i]);
        }
        for (int i = 0; i < arr1.length; i++) {
            for (int j = 0; j < arr1.length; j++) {
                if (arr1[i] < arr1[j]) {
                    temp = arr1[i];
                    arr1[i] = arr1[j];
                    arr1[j] = temp;
                }
            }
        }
        System.out.println("Sorted Array");
        for (int i = 0; i < arr1.length; i++) {
            System.out.println(arr1[i]);
        }
    }
}