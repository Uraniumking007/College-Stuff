import java.util.Scanner;

class p5a {
    public static void main(String args[]) {
        int choice, n;
        Scanner input = new Scanner(System.in);
        System.out.println("Enter largest number in Sequence: ");
        n = input.nextInt();
        System.out.println("Enter 1. for Ascending Order\nEnter 2. for Descending Order\n Enter you choice: ");
        choice = input.nextInt();
        System.out.println("\n\n");

        switch (choice) {
            case 1:
                ascending(n);
                break;
            case 2:
                descending(n);
                break;

            default:
                break;
        }
    }

    public static void ascending(int a) {
        int i = 1;
        while (i <= a) {
            System.out.println(i);
            i++;
        }
    }

    public static void descending(int a) {
        int i = a;
        while (i > 0) {
            System.out.println(i);
            i--;
        }
    }
}

/**
 * p5b
 */
class p5b {
    public static void main(String args[]) {
        int n;
        Scanner input = new Scanner(System.in);
        System.out.println("Enter a Number: ");
        n = input.nextInt();
        for (int i = 0; i < 3; i++) {
            int digit;
            digit = n % 10;
            n /= 10;
            System.out.println(digit);
        }
    }
}

class p5c {
    public static void main(String args[]) {
        int i = 100;
        do {
            if (i % 5 == 0) {
                
                    System.out.println(i);
                    
                }
                i++;
            } while (i <= 1000);
    }
}
class p5d   {
    public static void main(String args[]) {
        int a;
        Scanner input = new Scanner(System.in);
        System.out.println("Enter a Number");
        a = input.nextInt();
        int flag = 0;
        for (int i = 1; i <= a/2; i++) {
            if (a%i==0) {
                flag++;
                if (flag>1) {
                    break;
                }
            }
        }
        if(flag > 1){
            System.out.println("It is not Prime Number");
        }
        else{
        
        System.out.println("It is Prime Number");
        }

    }
}

class p5b_1 {
    public static void main(String args[]) {
        int n;
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter a Number: ");
        n = sc.nextInt();
        String str_no = Integer.toString(n);
        for (int i = 0; i < str_no.length(); i++) {
            System.out.println(str_no.charAt(i));
        }
    }
}
