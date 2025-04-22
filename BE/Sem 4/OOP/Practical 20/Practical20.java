interface Function {
    int evaluate(int x);
}

class Half implements Function {
    @Override
    public int evaluate(int x) {
        return x / 2;
    }
}

public class Practical20 {
    public static void main(String[] args) {
        Function half = new Half();
        
        System.out.println("Half of 10 is: " + half.evaluate(10));
        System.out.println("Half of 7 is: " + half.evaluate(7));
        System.out.println("Half of -4 is: " + half.evaluate(-4));
        System.out.println("Half of 0 is: " + half.evaluate(0));
    }
}
