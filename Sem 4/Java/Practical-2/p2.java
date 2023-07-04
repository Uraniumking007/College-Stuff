import java.io.*;


class square{
    public static void main(String args[]) {
        int a,b;
        a = 10;
        b = a * a;
        System.out.println("Area of Square: "+b);

    }
}
class triangle{
    public static void main(String args[]) {
        double a,b,d;
        a = 10;
        b = 20;
        d = 0.5 * a * b;
        System.out.println("Area of Triangle: "+d);

    }
}
class ascii{
    public static void main(String args[]) {
        char a;
        int b;
        a = 'z';
        b = a;

        System.out.println("ASCII of "+a+": "+b);
    }
}
class cTof{
    public static void main(String args[]) {
        double f,c;
        c = 37;
        f = ( c * 1.8 ) + 32;
        System.out.println(f);
    }
}
class percentage{
    public static void main(String args[]) {
        double s1,s2,s3,r;
        s1 = 45;
        s2 = 46;
        s3 = 47;

        r = ((s1 + s2+ s3)/150) * 100;
        System.out.println(r);
    }
}