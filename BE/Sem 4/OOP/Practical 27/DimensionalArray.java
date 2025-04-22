public class DimensionalArray {
    public static <T extends Comparable<T>> T findMin(T[][] array) {
        if (array == null || array.length == 0 || array[0].length == 0) {
            return null;
        }

        T min = array[0][0];
        for (T[] row : array) {
            for (T element : row) {
                if (element.compareTo(min) < 0) {
                    min = element;
                }
            }
        }
        return min;
    }

    public static void main(String[] args) {
        // Example usage with Integer array
        Integer[][] intArray = {
                { 5, 2, 9 },
                { 1, 7, 6 },
                { 8, 3, 4 }
        };
        System.out.println("Minimum element in Integer array: " + findMin(intArray));

        // Example usage with Double array
        Double[][] doubleArray = {
                { 5.5, 2.1, 9.9 },
                { 1.2, 7.3, 6.4 },
                { 8.8, 3.2, 4.7 }
        };
        System.out.println("Minimum element in Double array: " + findMin(doubleArray));
    }
}