public class practical3 {
    public static String encrypt(String plaintext, String key) {
        StringBuilder ciphertext = new StringBuilder();
        plaintext = plaintext.toUpperCase();
        key = key.toUpperCase();
        int keyIndex = 0; for (char ch : plaintext.toCharArray()) {
            if (Character.isLetter(ch)) { char encryptedChar = (char) ((ch + key.charAt(keyIndex) - 2 * 'A') % 26 + 'A'); ciphertext.append(encryptedChar); keyIndex = (keyIndex + 1) % key.length();
            } else { ciphertext.append(ch);
            }
        }
        return ciphertext.toString();
    }
    public static String decrypt(String ciphertext, String key) {
        StringBuilder plaintext = new StringBuilder(); ciphertext = ciphertext.toUpperCase(); key = key.toUpperCase(); int keyIndex = 0; for (char ch : ciphertext.toCharArray()) {
            if (Character.isLetter(ch)) { char decryptedChar = (char) ((ch - key.charAt(keyIndex) + 26) % 26 + 'A');
                plaintext.append(decryptedChar); keyIndex = (keyIndex + 1) % key.length();
            } else { plaintext.append(ch);
            }
        } return plaintext.toString();
    }
    public static void main(String[] args) {
        String plaintext = "Adnan";
        String key = "KEY";
        String encryptedText = encrypt(plaintext, key);
        System.out.println("Encrypted: " + encryptedText);
        String decryptedText = decrypt(encryptedText, key);
        System.out.println("Decrypted: " + decryptedText);
    }
}
