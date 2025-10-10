import java.io.*;

public class extra {
    public static void main(String args[]) {
        int i=10,j=20;
        int k=i++ + --j;
        int l= ++i;
        System.out.println("i= "+i+"j= "+j+"k= "+k+"l= "+l);
        cube(i);
        ternary();
    }
    static void cube(int s) {
        int area;
        area= s*s*s;
        System.out.println("Area of cube: "+area);
    }
    static void ternary()   {
        int a,b=25;
        a = ( b == 25 ) ? 10 : 25;
        System.out.println("Value of : "+a);
    }
    
}