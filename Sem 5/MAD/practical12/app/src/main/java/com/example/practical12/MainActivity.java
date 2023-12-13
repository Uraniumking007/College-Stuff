package com.example.practical12;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;

public class MainActivity extends AppCompatActivity {

    Button btnAddTaskView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        btnAddTaskView = findViewById(R.id.addTaskViewButton);
        btnAddTaskView.setOnClickListener(v -> {
            Intent i = new Intent(MainActivity.this, AddTask.class);
            startActivity(i);
        });
    }
}