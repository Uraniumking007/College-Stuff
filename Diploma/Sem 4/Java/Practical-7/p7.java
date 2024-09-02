import java.util.Scanner;

class StrLen {
    public static void main(String[] args) {
        String str = "Bhavesh", str1;
        Scanner input = new Scanner(System.in);
        System.out.println("Enter a String");
        str1 = input.nextLine();
        System.out.println("Length Of Str1: " + str1.length());
        System.out.println("Length of Str" + str.length());
    }
}

class vowels {
    public static void main(String[] args) {
        int count = 0;
        String str = "I am Bhavesh";
        for (int i = 0; i < str.length(); i++) {
            char a = str.charAt(i);
            if (a == 'a' || a == 'i' || a == 'e' || a == 'o' || a == 'u') {
                count++;
            }
        }
        System.out.println("No .of Vowels: " + count);
    }
}

class Palindrome {
    public static void main(String[] args) {
        String str1 = "MOM";
        System.out.println(str1);
        int count = 0;
        for (int i = 0; i < args.length; i++) {
            for (int j = (str1.length() - 1); j >= 0; j--) {
                if (str1.charAt(i) == str1.charAt(j)) {
                    count++;
                }
            }
        }
        if (count == str1.length()) {
            System.out.println("String is Palindrome");
        } else {
            System.out.println("String is not Palindrome");
        }
    }
}