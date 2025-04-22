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

    public ColorChangeCircle() {
        // Default constructor is required by JavaFX
    }

    @Override
    public void start(Stage stage) {
        Circle circle = new Circle(
            WINDOW_WIDTH / 2,
            WINDOW_HEIGHT / 2,
            CIRCLE_RADIUS,
                Color.BLUE
        );

        Pane pane = new Pane();
        pane.getChildren().add(circle);

        Scene scene = new Scene(pane, WINDOW_WIDTH, WINDOW_HEIGHT);

        pane.setOnMousePressed(event -> {
            circle.setFill(Color.RED);
        });

        pane.setOnMouseReleased(event -> {
            circle.setFill(Color.BLUE);
        });

        stage.setTitle("Color Changing Circle");
        stage.setScene(scene);
        stage.setResizable(false);
        stage.show();
    }

    public static void main(String[] args) {
        launch();
    }
}