/**
 * externalpractical
 */
public class externalpractical {

    public String ALPHABETS = "abcdefghijklmnopqrstuvwxyz";

    String encrypt(String plainText, int key) {
        plainText = plainText.toLowerCase();
        String encryptedString = "";
        for (int i = 0; i < plainText.length(); i++) {
            int index = ALPHABETS.indexOf(plainText.charAt(i));
            int encryptedValueInt = (index + key) % 26;
            encryptedString += ALPHABETS.charAt(encryptedValueInt);
        }
        return encryptedString;
    }

    public static void main(String[] args) {
        externalpractical e = new externalpractical();
        String plainText = "Helloo";
        int key = 3;
        String encryptedString = e.encrypt(plainText, key);
        System.out.println("Plain Text String: " + plainText);
        System.out.println("Key: " + key);
        System.out.println("Encrypted Text String: " + encryptedString);

    }

}