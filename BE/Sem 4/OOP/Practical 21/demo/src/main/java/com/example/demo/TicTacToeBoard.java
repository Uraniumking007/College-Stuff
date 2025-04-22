package com.example.demo;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.layout.GridPane;
import javafx.stage.Stage;
import javafx.geometry.Pos;
import java.util.Random;

public class TicTacToeBoard extends Application {
    private static final int BOARD_SIZE = 3;
    private static final int CELL_SIZE = 100;
    
    @Override
    public void start(Stage stage) {
        GridPane gridPane = new GridPane();
        gridPane.setHgap(2);
        gridPane.setVgap(2);
        gridPane.setStyle("-fx-background-color: black;");

        Random random = new Random();

        for (int row = 0; row < BOARD_SIZE; row++) {
            for (int col = 0; col < BOARD_SIZE; col++) {
                Label cell = new Label();
                cell.setPrefSize(CELL_SIZE, CELL_SIZE);
                cell.setStyle("-fx-background-color: white; -fx-font-size: 40px; -fx-font-weight: bold;");
                cell.setAlignment(Pos.CENTER);
                
                int choice = random.nextInt(3); // 0: empty, 1: X, 2: O
                if (choice == 1) {
                    cell.setText("X");
                } else if (choice == 2) {
                    cell.setText("O");
                }
                
                gridPane.add(cell, col, row);
            }
        }

        Scene scene = new Scene(gridPane);
        stage.setTitle("Tic-Tac-Toe Board");
        stage.setScene(scene);
        stage.show();
    }

    public static void main(String[] args) {
        launch();
    }
}