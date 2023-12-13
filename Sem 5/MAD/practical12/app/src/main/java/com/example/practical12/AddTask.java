package com.example.practical12;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.Toast;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

public class AddTask extends AppCompatActivity {

private    EditText taskName, taskDescription;
    private CheckBox isCompleted;
    private Button addTaskBtn;
    private FirebaseDatabase db;
    private DatabaseReference reference;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_task);
        taskName = findViewById(R.id.taskNameEdit);
        taskDescription = findViewById(R.id.taskDescriptionEdit);
        isCompleted = findViewById(R.id.checkBox);
        addTaskBtn = findViewById(R.id.addTaskBtn);
        db = FirebaseDatabase.getInstance();
        reference = db.getReference("tasks");

        addTaskBtn.setOnClickListener(v -> {
            String name = taskName.getText().toString();
            String description = taskDescription.getText().toString();
            boolean completed = isCompleted.isChecked();
            String taskId = reference.push().getKey();
            TaskRVModal task = new TaskRVModal(taskId,name, description, completed);
            reference.addValueEventListener(new ValueEventListener() {
                @Override
                public void onDataChange(@NonNull DataSnapshot snapshot) {
                    reference.child(taskId).setValue(task);
                    Toast.makeText(AddTask.this, "Task Added", Toast.LENGTH_SHORT).show();
                    Intent intent = new Intent(AddTask.this, MainActivity.class);
                    startActivity(intent);
                }

                @Override
                public void onCancelled(@NonNull DatabaseError error) {
                    Toast.makeText(AddTask.this, "Failed to add task", Toast.LENGTH_SHORT).show();
                }
            });
        });

    }
}