package com.example.demo;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.layout.Pane;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.stage.Stage;

public class ColorChangeCircle extends Application {
    private static final int WINDOW_WIDTH = 400;
    private static final int WINDOW_HEIGHT = 400;
    private static final int CIRCLE_RADIUS = 50;

    // Add a default constructor
    public ColorChangeCircle() {
        // Default constructor is required by JavaFX
    }

    @Override
    public void start(Stage stage) {
        // Create a circle in the center of the window
        Circle circle = new Circle(
            WINDOW_WIDTH / 2,  // Center X
            WINDOW_HEIGHT / 2, // Center Y
            CIRCLE_RADIUS,     // Radius
            Color.BLUE        // Initial color
        );

        // Create a pane and add the circle to it
        Pane pane = new Pane();
        pane.getChildren().add(circle);

        // Create the scene
        Scene scene = new Scene(pane, WINDOW_WIDTH, WINDOW_HEIGHT);

        // Add mouse event handlers for the entire pane
        pane.setOnMousePressed(event -> {
            circle.setFill(Color.RED);
        });

        pane.setOnMouseReleased(event -> {
            circle.setFill(Color.BLUE);
        });

        // Set up the stage
        stage.setTitle("Color Changing Circle");
        stage.setScene(scene);
        stage.setResizable(false);
        stage.show();
    }

    public static void main(String[] args) {
        launch();
    }
}