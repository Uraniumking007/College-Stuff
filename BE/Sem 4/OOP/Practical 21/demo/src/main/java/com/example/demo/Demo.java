package com.example.demo;

import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.scene.text.Text;
import javafx.stage.Stage;

public class Demo extends Application {
    private static final int WINDOW_WIDTH = 500;
    private static final int WINDOW_HEIGHT = 300;
    private static final int MOVEMENT_DELTA = 10;
    private double textX = WINDOW_WIDTH / 2.0;

    public Demo() {
        // Default constructor required by JavaFX
    }

    @Override
    public void start(Stage stage) {
        Text message = new Text("Hello, World!");
        message.setX(textX);
        message.setY(100);

        Button leftButton = new Button("Move Left");
        Button rightButton = new Button("Move Right");

        RadioButton redButton = new RadioButton("Red");
        RadioButton blueButton = new RadioButton("Blue");
        RadioButton greenButton = new RadioButton("Green");

        ToggleGroup colorGroup = new ToggleGroup();
        redButton.setToggleGroup(colorGroup);
        blueButton.setToggleGroup(colorGroup);
        greenButton.setToggleGroup(colorGroup);
        redButton.setSelected(true);
        message.setFill(Color.RED);

        HBox buttonBox = new HBox(10);
        buttonBox.setAlignment(Pos.CENTER);
        buttonBox.getChildren().addAll(leftButton, rightButton);

        HBox radioBox = new HBox(10);
        radioBox.setAlignment(Pos.CENTER);
        radioBox.getChildren().addAll(redButton, blueButton, greenButton);

        VBox root = new VBox(20);
        root.setPadding(new Insets(15));
        root.setAlignment(Pos.CENTER);
        root.getChildren().addAll(message, buttonBox, radioBox);

        leftButton.setOnAction(e -> {
            if (message.getX() - MOVEMENT_DELTA >= 0) {
                message.setX(message.getX() - MOVEMENT_DELTA);
            }
        });

        rightButton.setOnAction(e -> {
            if (message.getX() + MOVEMENT_DELTA + message.getLayoutBounds().getWidth() <= WINDOW_WIDTH) {
                message.setX(message.getX() + MOVEMENT_DELTA);
            }
        });

        redButton.setOnAction(e -> message.setFill(Color.RED));
        blueButton.setOnAction(e -> message.setFill(Color.BLUE));
        greenButton.setOnAction(e -> message.setFill(Color.GREEN));

        Scene scene = new Scene(root, WINDOW_WIDTH, WINDOW_HEIGHT);

        stage.setTitle("Message Mover");
        stage.setScene(scene);
        stage.setResizable(false);
        stage.show();
    }

    public static void main(String[] args) {
        launch();
    }
}