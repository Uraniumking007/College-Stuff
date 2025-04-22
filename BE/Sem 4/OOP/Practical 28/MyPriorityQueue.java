import java.util.PriorityQueue;

public class MyPriorityQueue extends PriorityQueue<Integer> implements Cloneable {

    public MyPriorityQueue() {
        super();
    }

    @Override
    public MyPriorityQueue clone() {
        MyPriorityQueue clone = new MyPriorityQueue();
        clone.addAll(this);
        return clone;
    }

    public static void main(String[] args) {
        MyPriorityQueue pq = new MyPriorityQueue();

        pq.add(5);
        pq.add(2);
        pq.add(8);
        pq.add(1);

        System.out.println("Original queue: " + pq);

        MyPriorityQueue clonedPq = pq.clone();

        System.out.println("Cloned queue: " + clonedPq);

        System.out.println("Polling from original queue: " + pq.poll());

        System.out.println("Original queue after poll: " + pq);
        System.out.println("Cloned queue remains unchanged: " + clonedPq);
    }
}
