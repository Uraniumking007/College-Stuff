import java.util.Scanner;

class Trip {
    // String sourceArr[] = { "Surat", "Baroda", "Bardoli", "Mumbai" };
    // String destinationArr[] = { "Surat", "Baroda", "Bardoli", "Mumbai" };
    String source, destination, date;
    int days;

    Trip(String src, String des, String dte, int dys) {
        source = src;
        destination = des;
        date = dte;
        days = dys;
    }

    void bookNow(String variable) {
        System.out.println("Booking Confirmed on " + variable + ".");
    }

    void showDetails() {
        System.out.println("Enter Source: " + source);
        System.out.println("Enter Destination: " + destination);
        System.out.println("Enter Start Date: " + date);
        System.out.println("Enter Total days: " + days);
    }

    public static void main(String[] args) {
        String src;
        String des;
        String dte;
        int dys, choice = 1;
        Scanner sc = new Scanner(System.in);
        System.out.println("Welcome to the Booking System");
        System.out.println("Enter Source: ");
        src = sc.next();
        System.out.println("Enter Destination: ");
        des = sc.next();
        System.out.println("Enter Date: ");
        dte = sc.next();
        System.out.println("No. of Days");
        dys = sc.nextInt();
        while (choice != 0) {
            System.out
                    .println("Please enter your choice from below options:\n 1. Show Details\n 2. Book Now\n 0. Exit");
            choice = sc.nextInt();
            Trip x = new Trip(src, des, dte, dys);
            switch (choice) {
                case 1:
                    x.showDetails();
                    break;
                case 2:
                    x.bookNow(dte);
                    break;
                case 0:
                    System.out.println("Exited");
                    break;
                default:
                    System.out.println("Invalid Choice");
                    break;
            }

        }

    }
}