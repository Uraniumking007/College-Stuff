public class Rectangle {
    private int length;
    private int width;
    
    public Rectangle() {
        this.length = 0;
        this.width = 0;
    }
    
    public int getLength() {
        return length;
    }
    
    public void setLength(int length) {
        this.length = length;
    }
    
    public int getWidth() {
        return width;
    }
    
    public void setWidth(int width) {
        this.width = width;
    }
    
    public int getArea() {
        return length * width;
    }
    
    public static void main(String[] args) {
        Rectangle rectangle = new Rectangle();
        System.out.println("Default rectangle - Length: " + rectangle.getLength() + 
                ", Width: " + rectangle.getWidth() + 
                ", Area: " + rectangle.getArea());
        
        rectangle.setLength(5);
        rectangle.setWidth(10);
        
        System.out.println("After setting dimensions - Length: " + rectangle.getLength() +
                ", Width: " + rectangle.getWidth() + 
                ", Area: " + rectangle.getArea());
        
        Rectangle rectangle2 = new Rectangle();
        rectangle2.setLength(7);
        rectangle2.setWidth(3);
        System.out.println("Second rectangle - Length: " + rectangle2.getLength() + 
                ", Width: " + rectangle2.getWidth() + 
                ", Area: " + rectangle2.getArea());
    }
}
