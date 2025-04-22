public class P2 {
    public static void main(String[] args) {
        double a = 3.4;
        double b = 50.2;
        double c = 2.1;
        double d = 0.55;
        double e = 44.5;
        double f = 5.9;

        double determinant = a * d - b * c;

        double x = (e * d - b * f) / determinant;

        double y = (a * f - e * c) / determinant;

        System.out.printf("x = %.2f\n", x);
        System.out.printf("y = %.2f\n", y);
    }
}