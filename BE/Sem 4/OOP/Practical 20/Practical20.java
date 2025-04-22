/**
 * Practical 20
 * 
 * This program demonstrates the implementation of a Function interface
 * with a Half class that divides an integer value by 2.
 */

// Interface that defines a function which takes an int and returns an int
interface Function {
    int evaluate(int x);
}

// Implementation of the Function interface that returns half of the input value
class Half implements Function {
    @Override
    public int evaluate(int x) {
        return x / 2;
    }
}

public class Practical20 {
    public static void main(String[] args) {
        // Create an instance of the Half class
        Function half = new Half();
        
        // Test the evaluate method with different values
        System.out.println("Half of 10 is: " + half.evaluate(10));
        System.out.println("Half of 7 is: " + half.evaluate(7));
        System.out.println("Half of -4 is: " + half.evaluate(-4));
        System.out.println("Half of 0 is: " + half.evaluate(0));
        
        // Note: This uses integer division, so half of 7 will be 3 (not 3.5)
    }
}
