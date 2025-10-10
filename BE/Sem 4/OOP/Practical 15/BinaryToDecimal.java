
public class BinaryToDecimal {
    public static int bin2Dec(String binaryString) throws NumberFormatException {
        if (binaryString == null || binaryString.isEmpty()) {
            throw new NumberFormatException("Binary string cannot be null or empty");
        }
        for (char ch : binaryString.toCharArray()) {
            if (ch != '0' && ch != '1') {
                throw new NumberFormatException("Binary string can only contain 0s and 1s");
            }
        }

        int decimal = 0;
        for (int i = 0; i < binaryString.length(); i++) {
            decimal = decimal << 1; // Same as decimal * 2
            if (binaryString.charAt(i) == '1') {
                decimal += 1;
            }
        }

        return decimal;
    }

    public static void main(String[] args) {
        String[] testBinaries = { "1010", "1111", "10000", "abc", "", null };

        for (String binary : testBinaries) {
            try {
                int decimal = bin2Dec(binary);
                System.out.println("Binary: " + binary + " -> Decimal: " + decimal);
            } catch (NumberFormatException e) {
                System.out.println("Error: " + e.getMessage());
            }
        }
    }
}
