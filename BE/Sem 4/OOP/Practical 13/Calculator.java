public class Calculator {
    int calc(String str) {
        String[] x;
        if (str.contains(" ")) {
            x = str.split(" ");

        } else {
            x = str.split("");

        }
        int a = Integer.parseInt(x[0]);
        int b = Integer.parseInt(x[2]);
        switch (x[1]) {
            case "+":
                return a + b;

            case "-":
                return a - b;

            case "*":
                return a * b;

            case "/":
                return a / b;

            default:
                System.out.println("Invalid operator");
                return 0;
        }
    }

    public static void main(String[] args) {
        Calculator c = new Calculator();
        System.out.println(c.calc("5 + 5"));
        System.out.println(c.calc("5 - 5"));
        System.out.println(c.calc("5 * 5"));
        System.out.println(c.calc("5 / 5"));
        System.out.println(c.calc("5+5"));
        System.out.println(c.calc("5-5"));
        System.out.println(c.calc("5*5"));
        System.out.println(c.calc("5/5"));
    }
}
