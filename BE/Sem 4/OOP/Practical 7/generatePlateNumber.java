public class generatePlateNumber {

    public static void main(String[] args) {

        String letters = "";
        for (int i = 0; i < 3; i++) {
            letters += (char)(Math.random() * 26 + 'A');
        }
        
        int number = (int)(Math.random() * 10000);
        String digits = String.format("%04d", number);
        
        String plateNumber = letters + digits;
        
        System.out.println("Generated Plate Number: " + plateNumber);
    }
}