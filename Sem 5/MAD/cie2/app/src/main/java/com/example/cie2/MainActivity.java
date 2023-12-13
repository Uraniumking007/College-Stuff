package com.example.cie2;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.FragmentManager;

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
        linr = findViewById(R.id.linearLayout);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        MenuInflater mni =getMenuInflater();
        mni.inflate(R.menu.menu, menu);
        return super.onCreateOptionsMenu(menu);
    }

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {

        FragmentManager fm = getSupportFragmentManager();

if (item.getItemId() == R.id.profile){
    fm.beginTransaction().replace(R.id.profileFragment, Frangment1.class,null).setReorderingAllowed(true).addToBackStack("Hello").commit();
}
if (item.getItemId() == R.id.home){
    fm.beginTransaction().remove(getSupportFragmentManager().findFragmentById(R.id.profileFragment)).commit();
}
        return super.onOptionsItemSelected(item);
    }
}