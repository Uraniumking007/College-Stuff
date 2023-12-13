import java.util.*;

public class practical2 {
    private char[][] matrix = new char[5][5];

    public practical2(String key) {
        initializeMatrix(key);
    }

    private void initializeMatrix(String key) {
        Set<Character> usedChars = new HashSet<>();
        int row = 0, col = 0;
        for (char c : (key + "ABCDEFGHIKLMNOPQRSTUVWXYZ").toCharArray()) {
            c = (c == 'J') ? 'I' : c;
            if (!usedChars.contains(c)) {
                matrix[row][col] = c;
                usedChars.add(c);
                col = (col + 1) % 5;
                if (col == 0) {
                    row = (row + 1) % 5;
                }
            }
        }
    }

    private String preprocessText(String text) {
        text = text.replaceAll("[^A-Z]", "").replaceAll("J", "I");
        text = text.replaceAll("(.)\\1", "$1X$1");
        return (text.length() % 2 == 1) ? text + "X" : text;
    }

    private int[] findPosition(char c) {
        for (int i = 0; i < 5; i++) {
            for (int j = 0; j < 5; j++) {
                if (matrix[i][j] == c) {
                    return new int[]{i, j};
                }
            }
        }
        return null;
    }

    public String encrypt(String plaintext) {
        plaintext = preprocessText(plaintext);
        StringBuilder ciphertext = new StringBuilder();
        for (int i = 0; i < plaintext.length(); i += 2) {
            char c1 = plaintext.charAt(i);
            char c2 = plaintext.charAt(i + 1);
            int[] pos1 = findPosition(c1);
            int[] pos2 = findPosition(c2);
            int row1 = pos1[0], col1 = pos1[1];
            int row2 = pos2[0], col2 = pos2[1];
            if (row1 == row2) {
                ciphertext.append(matrix[row1][(col1 + 1) % 5]);
                ciphertext.append(matrix[row2][(col2 + 1) % 5]);
            } else if (col1 == col2) {
                ciphertext.append(matrix[(row1 + 1) % 5][col1]);
                ciphertext.append(matrix[(row2 + 1) % 5][col2]);
            } else {
                ciphertext.append(matrix[row1][col2]);
                ciphertext.append(matrix[row2][col1]);
            }
        }
        return ciphertext.toString();
    }

    public static void main(String[] args) {
        String key = "KEYWORD";
        String plaintext = "JODHUNME";
        practical2 cipher = new practical2(key);
        String encryptedText = cipher.encrypt(plaintext);
        System.out.println("Key: " + key);
        System.out.println("PlainText: " + plaintext);
        System.out.println("Encrypted Text: " + encryptedText);
    }
}
