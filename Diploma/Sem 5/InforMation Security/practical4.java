
import java.util.Arrays;
import java.util.Scanner;

class RailFence {
    public static String encryptRailFence(String text, int key) {
        char[][] rail = new char[key][text.length()];
        for (int i = 0; i < key; i++)
            Arrays.fill(rail[i], '\n');
        boolean dirDown = false;
        int row = 0, col = 0;
        for (int i = 0; i < text.length(); i++) {
            if (row == 0 || row == key - 1)
                dirDown = !dirDown;
            rail[row][col++] = text.charAt(i);
            if (dirDown)
                row++;
            else
                row--;
        }
        StringBuilder result = new StringBuilder();
        for (int i = 0; i < key; i++) {
            for (int j = 0; j < text.length(); j++) {
                if (rail[i][j] != '\n') {
                    result.append(rail[i][j]);
                } else {
                    result.append(' ');
                }
            }
            result.append('\n');
        }
        return result.toString();
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter the text to encrypt: ");
        String text = scanner.nextLine();
        System.out.print("Enter the key: ");
        int key = scanner.nextInt();
        scanner.close();
        String encryptedMessage = encryptRailFence(text, key);
        System.out.println("Encrypted Message: ");
        System.out.println(encryptedMessage);
    }
}