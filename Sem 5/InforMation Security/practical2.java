/**
 * playfaircypher
 */
public class pr2 {
    static String ALPHABETS = "abcdefghijklmnopqrstuvwxyz";

    public static void main(String[] args) {
        int charVal = 0;
        String plainStringMatrix[] = new String[20];
        String plainText = "MANHATTAN";
        int plainTextLen = plainText.length();
        if (plainTextLen % 2 != 0) {
            plainText = plainText + 'x';
            System.out.println(plainText);
        }
        int k = 0;
        int j= 0;
        for (int i = 0; i < plainTextLen - 1; i++) {
            if(j<plainTextLen){

                System.out.println(plainText.substring(j, j + 2));
                j+=2;
            }
        }
        // for (int i = 0; i < plainTextLen - 1; i++) {
        //     if(j<plainTextLen){

        //         plainStringMatrix[i] = plainText.substring(j, j + 2);
        //         j = j+2;
        //     }
        // }

        // Character matrix[][] = new Character[5][5];
        // ALPHABETS = ALPHABETS.toString();
        // for (int i = 0; i < 5; i++) {
        // for (int j = 0; j < 5; j++) {
        // if(ALPHABETS.charAt(charVal) == 'j'){
        // matrix[i][j-1] = (char) ('i');
        // charVal++;
        // matrix[i][j] = ALPHABETS.charAt(charVal);
        // charVal++;
        // } else{
        // matrix[i][j] = ALPHABETS.charAt(charVal);
        // charVal++;
        // }
        // }
        // }
        // for (int i = 0; i < 5; i++) {
        // for (int j = 0; j < 5; j++) {
        // // matrix[i][j] = ALPHABETS.charAt(charVal);
        // System.out.println(matrix[i][j]);
        // }
        // }
    }
}
