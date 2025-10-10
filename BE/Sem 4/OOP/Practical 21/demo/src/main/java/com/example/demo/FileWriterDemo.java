package com.example.demo;

import java.io.*;
import java.util.Random;

public class FileWriterDemo {
    public static void main(String[] args) {
        writeToFile();
        readFromFile();
    }

    private static void writeToFile() {
        String fileName = "123.txt";
        Random random = new Random();

        try (FileWriter fileWriter = new FileWriter(fileName, true);
             BufferedWriter bufferedWriter = new BufferedWriter(fileWriter)) {

            for (int i = 0; i < 150; i++) {
                int randomNumber = random.nextInt(1000);
                bufferedWriter.write(String.valueOf(randomNumber));
                bufferedWriter.write(" ");

                if ((i + 1) % 10 == 0) {
                    bufferedWriter.newLine();
                }
            }

            System.out.println("Successfully wrote 150 random integers to " + fileName);

        } catch (IOException e) {
            System.err.println("Error writing to file: " + e.getMessage());
            e.printStackTrace();
        }
    }

    private static void readFromFile() {
        String fileName = "123.txt";

        try (BufferedReader reader = new BufferedReader(new FileReader(fileName))) {
            System.out.println("\nContents of " + fileName + ":");
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }

        } catch (IOException e) {
            System.err.println("Error reading from file: " + e.getMessage());
            e.printStackTrace();
        }
    }
}