import java.util.Arrays;

/**
 * playfaircypher
 */
public class pr2 {
    static String ALPHABETS = "abcdefghijklmnopqrstuvwxyz";

    public static void main(String[] args) {

        String plainText = "MANHATTAN";
        int plainTextLen = plainText.length();

        pr2 p = new pr2();
        String jod = p.removeDuplicate(plainText);
        p.Matrix(jod);

        System.out.println(jod);

        // adding x at end if plaintext is odd
        // if (plainTextLen % 2 != 0) {
        // plainText = plainText + 'x';
        // System.out.println(plainText);
        // }
        // int k = 0;
        // int j = 0;

        // // Display pairs of 2 in plaintext
        // for (int i = 0; i < plainTextLen - 1; i++) {
        // if (j < plainTextLen) {

        // System.out.println(plainText.substring(j, j + 2));
        // j += 2;
        // }
        // }
        // for (int i = 0; i < plainTextLen - 1; i++) {
        // if(j<plainTextLen){

        // plainStringMatrix[i] = plainText.substring(j, j + 2);
        // j = j+2;
        // }
        // }
    }

    String removeDuplicate(String str) {
        int j, index = 0;
        char[] c = str.toCharArray();
        for (int i = 0; i < str.length(); i++) {
            for (j = 0; j < str.length(); j++) {
                if (c[i] == c[j]) {
                    break;
                }
            }
            if (i == j) {
                c[index++] = c[j];
            }
        }
        String l = new String(Arrays.copyOf(c, index));
        return l;
    }

    String removeSpace(String str) {

    }

    void Matrix(String str) {
        int charVal = 0, k = str.length();
        String plainStringMatrix[] = new String[20];
        Character matrix[][] = new Character[5][5];
        char[] martixArray = new char[70];
        str = str.toLowerCase();

        for (int i = 0; i < str.length(); i++) {
            martixArray[i] = str.charAt(i);
        }

        for (int i = 0; i < martixArray.length; i++) {
            String c = str.charAt(i);
            ALPHABETS.replaceAll(c, " ");
        }
        String abc = ALPHABETS;
        abc = abc.replaceAll(" ", "");
        System.out.println(abc);

        // for (int i = 0; i < matrix.length; i++) {
        // for (int j = 0; j < str.length(); j++) {

        // if (ALPHABETS.charAt(i) == martixArray[j]) {
        // break;
        // } else {
        // }
        // }
        // martixArray[k] = ALPHABETS.charAt(i);
        // k++;
        // }
        // for (int i = 0; i < martixArray.length; i++) {
        // System.out.println(martixArray[i]);
        // }

        // for (int i = 0; i < 5; i++) {
        // for (int j = 0; j < 5; j++) {
        // if (matrixArray.charAt(charVal) == 'j') {
        // matrix[i][j - 1] = (char) ('i');
        // charVal++;
        // matrix[i][j] = matrixArray.charAt(charVal);
        // charVal++;
        // } else {
        // matrix[i][j] = matrixArray.charAt(charVal);
        // charVal++;
        // }
        // }
        // }
        // for (int i = 0; i < 5; i++) {
        // for (int j = 0; j < 5; j++) {
        // // matrix[i][j] = ALPHABETS.charAt(charVal);
        // System.out.print(matrix[i][j]);
        // }
        // System.out.println(' ');
        // }
        // return matrix;
    }
}
