import java.util.*;
import java.io.*;


class extra1 {
    public static int l,b,k;
    public static void main(String args[]) {
        
        Scanner sc = new Scanner(System.in);
        l = sc.nextInt();
        b = sc.nextInt();
        if (l==b) {
            System.out.println("It is a Square");
        }
        else{
            System.out.println("It is not Square");
        }
    }    
}
class extra2{
    public static void main(String args[]) {
        int s,e,b;
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter Salary");
        s = sc.nextInt();
        System.out.println("Enter Exprience");
        e = sc.nextInt();
        if (e>5) {
            b=(10*s)/100;
            System.out.println("Your bonus: "+b);
        }
        else if (e>=2 && e<=5) {
            b=(5*s)/100;
            System.out.println("Your bonus: "+b);
        }
        else {
            b=(2*s)/100;
            System.out.println("Your bonus: "+b);
        }
    }
}
class extra3{
    public static void main(String args[]) {
        int a,h;
        float per;
        Scanner input = new Scanner(System.in);
        System.out.println("Number of Classes Held: ");
        h = input.nextInt();
        System.out.println("Number of Classes Attended: ");
        a = input.nextInt();
        per = ( a * 100 ) / h;
        System.out.println("Attendance: " +per + "%");
        if (per >= 75) {
            System.out.println("You can sit in Exam");
        } else {
            System.out.println("You cannot sit in Exam");
        }
    }
}