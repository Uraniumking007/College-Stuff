package com.example.demo;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.input.KeyCode;
import javafx.scene.layout.Pane;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.stage.Stage;

public class MoveCircle extends Application {
    private static final int WINDOW_WIDTH = 400;
    private static final int WINDOW_HEIGHT = 400;
    private static final int CIRCLE_RADIUS = 20;
    private static final int MOVEMENT_DELTA = 10;

    @Override
    public void start(Stage stage) {
        // Create a circle
        Circle circle = new Circle(
            WINDOW_WIDTH / 2, // Initial X position (center of window)
            WINDOW_HEIGHT / 2, // Initial Y position (center of window)
            CIRCLE_RADIUS, // Radius
            Color.RED // Color
        );

        // Create a pane and add the circle to it
        Pane pane = new Pane();
        pane.getChildren().add(circle);

        // Create the scene
        Scene scene = new Scene(pane, WINDOW_WIDTH, WINDOW_HEIGHT);

        // Add key event handler
        scene.setOnKeyPressed(event -> {
            switch (event.getCode()) {
                case UP:
                    // Check if moving up would keep the circle within bounds
                    if (circle.getCenterY() - MOVEMENT_DELTA >= CIRCLE_RADIUS) {
                        circle.setCenterY(circle.getCenterY() - MOVEMENT_DELTA);
                    }
                    break;
                case DOWN:
                    // Check if moving down would keep the circle within bounds
                    if (circle.getCenterY() + MOVEMENT_DELTA <= WINDOW_HEIGHT - CIRCLE_RADIUS) {
                        circle.setCenterY(circle.getCenterY() + MOVEMENT_DELTA);
                    }
                    break;
                case LEFT:
                    // Check if moving left would keep the circle within bounds
                    if (circle.getCenterX() - MOVEMENT_DELTA >= CIRCLE_RADIUS) {
                        circle.setCenterX(circle.getCenterX() - MOVEMENT_DELTA);
                    }
                    break;
                case RIGHT:
                    // Check if moving right would keep the circle within bounds
                    if (circle.getCenterX() + MOVEMENT_DELTA <= WINDOW_WIDTH - CIRCLE_RADIUS) {
                        circle.setCenterX(circle.getCenterX() + MOVEMENT_DELTA);
                    }
                    break;
            }
        });

        // Set up the stage
        stage.setTitle("Move Circle with Arrow Keys");
        stage.setScene(scene);
        stage.setResizable(false);
        stage.show();

        // Request focus on the scene so it can receive key events immediately
        pane.requestFocus();
    }

    public static void main(String[] args) {
        launch();
    }
}