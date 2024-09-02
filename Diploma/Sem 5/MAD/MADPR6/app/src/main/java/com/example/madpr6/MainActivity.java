package com.example.madpr6;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.Adapter;
import android.widget.AdapterView;
import android.widget.ImageView;
import android.widget.Spinner;

public class MainActivity extends AppCompatActivity implements AdapterView.OnItemSelectedListener {

    Spinner carSelect;
    ImageView img;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

         carSelect = findViewById(R.id.spinner);
         img = findViewById(R.id.imageView);
         carSelect.setOnItemSelectedListener(this);
    }

    @Override
    public void onItemSelected(AdapterView<?> adapterView, View view, int i, long l) {
        if(i == 0){
            img.setImageResource(R.drawable.bmw_m5);
        }
        if (i == 1){
            img.setImageResource(R.drawable.bmw_m3);
        }
        if(i == 2){
            img.setImageResource(R.drawable.porsche_911_carerra_rsr);
        }

    }

    @Override
    public void onNothingSelected(AdapterView<?> adapterView) {

    }
}