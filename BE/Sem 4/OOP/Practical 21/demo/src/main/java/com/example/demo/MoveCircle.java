package com.example.demo;

import javafx.application.Application;
import javafx.scene.Scene;
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
        Circle circle = new Circle(
            WINDOW_WIDTH / 2,
            WINDOW_HEIGHT / 2,
            CIRCLE_RADIUS,
            Color.RED
        );

        Pane pane = new Pane();
        pane.getChildren().add(circle);

        Scene scene = new Scene(pane, WINDOW_WIDTH, WINDOW_HEIGHT);

        scene.setOnKeyPressed(event -> {
            switch (event.getCode()) {
                case UP:
                    if (circle.getCenterY() - MOVEMENT_DELTA >= CIRCLE_RADIUS) {
                        circle.setCenterY(circle.getCenterY() - MOVEMENT_DELTA);
                    }
                    break;
                case DOWN:
                    if (circle.getCenterY() + MOVEMENT_DELTA <= WINDOW_HEIGHT - CIRCLE_RADIUS) {
                        circle.setCenterY(circle.getCenterY() + MOVEMENT_DELTA);
                    }
                    break;
                case LEFT:
                    if (circle.getCenterX() - MOVEMENT_DELTA >= CIRCLE_RADIUS) {
                        circle.setCenterX(circle.getCenterX() - MOVEMENT_DELTA);
                    }
                    break;
                case RIGHT:
                    if (circle.getCenterX() + MOVEMENT_DELTA <= WINDOW_WIDTH - CIRCLE_RADIUS) {
                        circle.setCenterX(circle.getCenterX() + MOVEMENT_DELTA);
                    }
                    break;
            }
        });

        stage.setTitle("Move Circle with Arrow Keys");
        stage.setScene(scene);
        stage.setResizable(false);
        stage.show();

        pane.requestFocus();
    }

    public static void main(String[] args) {
        launch();
    }
}