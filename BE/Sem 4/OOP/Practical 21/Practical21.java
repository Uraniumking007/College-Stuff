import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.layout.GridPane;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.stage.Stage;
import java.util.Random;

public class Practical21 extends Application {
    private static final int CELL_SIZE = 100;
    private static final int GRID_SIZE = 3;
    
    @Override
    public void start(Stage primaryStage) {
        // Create grid pane for the tic-tac-toe board
        GridPane gridPane = new GridPane();
        gridPane.setHgap(1);
        gridPane.setVgap(1);
        gridPane.setStyle("-fx-background-color: black; -fx-padding: 1;");
        
        // Load images
        Image xImage = new Image("X.gif");
        Image oImage = new Image("O.gif");
        
        // Random generator
        Random random = new Random();
        
        // Fill the grid with random X, O, or empty cells
        for (int row = 0; row < GRID_SIZE; row++) {
            for (int col = 0; col < GRID_SIZE; col++) {
                // Generate a random number (0, 1, or 2)
                // 0: Empty, 1: X, 2: O
                int cellContent = random.nextInt(3);
                
                ImageView imageView = new ImageView();
                imageView.setFitHeight(CELL_SIZE);
                imageView.setFitWidth(CELL_SIZE);
                
                switch (cellContent) {
                    case 1: // X
                        imageView.setImage(xImage);
                        break;
                    case 2: // O
                        imageView.setImage(oImage);
                        break;
                    default: // Empty
                        // Leave imageView empty but set a white background
                        break;
                }
                
                // Set a white background for all cells
                imageView.setStyle("-fx-background-color: white;");
                
                // Add to grid
                gridPane.add(imageView, col, row);
            }
        }
        
        // Create a scene and set it in the stage
        Scene scene = new Scene(gridPane);
        primaryStage.setTitle("Tic-Tac-Toe Board");
        primaryStage.setScene(scene);
        primaryStage.setResizable(false);
        primaryStage.show();
    }
    
    public static void main(String[] args) {
        launch(args);
    }
}
