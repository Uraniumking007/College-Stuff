/**
 * Rectangle class that provides functionality for rectangle operations
 */
public class Rectangle {
    // Fields
    private int length;
    private int width;
    
    /**
     * Default constructor that initializes length and width to 0
     */
    public Rectangle() {
        this.length = 0;
        this.width = 0;
    }
    
    /**
     * Calculates and returns the area of rectangle
     * @return area of rectangle (length × width)
     */
    public int getArea() {
        return length * width;
    }
}
