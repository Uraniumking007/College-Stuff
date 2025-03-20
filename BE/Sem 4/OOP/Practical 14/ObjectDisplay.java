import java.util.ArrayList;
import java.util.Date;

class ObjectDisplay {
    public static void main(String[] args) {
        ArrayList<Object> list = new ArrayList<>();
        list.add(new Loan(2.5, 1000));
        list.add(new Date());
        list.add("Hello World");
        list.add(new Circle(5.0));

        for (Object obj : list) {
            System.out.println(obj.toString());
        }
    }
}

class Loan {
    private double rate;
    private double amount;

    public Loan(double rate, double amount) {
        this.rate = rate;
        this.amount = amount;
    }

    @Override
    public String toString() {
        return "Loan [rate=" + rate + "%, amount=$" + amount + "]";
    }
}

class Circle {
    private double radius;

    public Circle(double radius) {
        this.radius = radius;
    }

    @Override
    public String toString() {
        return "Circle [radius=" + radius + "]";
    }
}