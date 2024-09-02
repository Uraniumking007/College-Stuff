package com.example.madp7;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.widget.LinearLayout;

public class MainActivity extends AppCompatActivity {
    LinearLayout linr;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        linr = findViewById(R.id.linr2);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        MenuInflater mm= getMenuInflater();
        mm.inflate(R.menu.mnnu,menu);
        return true;
    }


    @SuppressLint("ResourceAsColor")
    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {
        if(item.getItemId() == R.id.red) {
            linr.setBackgroundColor(R.color.red);
        }
        if (item.getItemId()==R.id.purple){
            linr.setBackgroundColor(R.color.purple);
        }
        if (item.getItemId()==R.id.white){
            linr.setBackgroundColor(R.color.white);
        }
        if (item.getItemId()==R.id.black){
            linr.setBackgroundColor(R.color.black);
        }

        return super.onOptionsItemSelected(item);
    }
}