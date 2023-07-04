class Box {
    int height, width, depth;

    Box(int a, int b, int c) {

        height = a;
        width = b;
        depth = c;
    }

    int vol() {
        return height * depth * width;
    }
}

public class p9 {
    public static void main(String[] args) {
        Box b = new Box(10, 10, 10);
        System.out.println("Volume of Box: " + b.vol());
    }
}
