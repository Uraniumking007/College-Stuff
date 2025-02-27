public class checkOddNumber {
    public static void main(String[] args) {
        int[][] matrix = new int[6][6];

        for (int i = 0; i < 6; i++) {
            for (int j = 0; j < 6; j++) {
                matrix[i][j] = (int)(Math.random() * 2);
            }
        }
        
        System.out.println("Generated Matrix:");
        for (int i = 0; i < 6; i++) {
            for (int j = 0; j < 6; j++) {
                System.out.print(matrix[i][j] + " ");
            }
            System.out.println();
        }
        
        System.out.println("\nChecking rows for odd number of 1's:");
        for (int i = 0; i < 6; i++) {
            int count = 0;
            for (int j = 0; j < 6; j++) {
                if (matrix[i][j] == 1) count++;
            }
            System.out.println("Row " + (i+1) + ": " + ((count % 2 == 1) ? "Has odd 1's" : "Has even 1's"));
        }
        
        System.out.println("\nChecking columns for odd number of 1's:");
        for (int j = 0; j < 6; j++) {
            int count = 0;
            for (int i = 0; i < 6; i++) {
                if (matrix[i][j] == 1) count++;
            }
            System.out.println("Column " + (j+1) + ": " + ((count % 2 == 1) ? "Has odd 1's" : "Has even 1's"));
        }
    }
}