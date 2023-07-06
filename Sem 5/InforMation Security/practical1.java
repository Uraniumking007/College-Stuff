// ceaser cipher

public class pr1 {
    public static String ALPHABET = "abcdefghijklmnopqrstuvwxyz";

    public static String encrypt(String plainText, int enkey) {

        String cypherText = "";

        for (int i = 0; i < plainText.length(); i++) {
            plainText = plainText.toLowerCase();
            int index = ALPHABET.indexOf(plainText.charAt(i));
            int encryptedValueInt = (index + enkey) % 26;
            cypherText += ALPHABET.charAt(encryptedValueInt);
        }
        return cypherText;
    }

    public static String decrypt(String encryptedValue, int enkey) {

        String decryptedValue = "";

        for (int i = 0; i < encryptedValue.length(); i++) {
            encryptedValue = encryptedValue.toLowerCase();
            int index = ALPHABET.indexOf(encryptedValue.charAt(i));
            int decryptedValueInt = (index - enkey) % 26;
            if (decryptedValueInt < 0) {
                decryptedValueInt += 26;
            }
            decryptedValue += ALPHABET.charAt(decryptedValueInt);
        }
        return decryptedValue;
    }

    public static void main(String[] args) {
        String PlainText = "information";
        String jod = encrypt(PlainText, 3);
        // String jodDec = decrypt("lqirupdwlrq", 3);
        String jodDec = decrypt(encrypt(PlainText, 3), 3);
        System.out.println(jod);
        System.out.println(jodDec);

    }
}
