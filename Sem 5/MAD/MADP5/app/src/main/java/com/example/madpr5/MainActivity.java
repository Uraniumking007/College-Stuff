package com.example.madpr5;

import androidx.appcompat.app.AppCompatActivity;

import android.app.SearchManager;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    EditText searchString;
    Button searchBtn;

    public String search;


    public void search(String search){
        if(search.isEmpty()){
            Toast.makeText(this, "Username & password are Required",Toast.LENGTH_SHORT).show();
        }else {
            defaultBrowser(search);
        }
    }
    private void defaultBrowser(String s){
        try {
            Intent i = new Intent(Intent.ACTION_WEB_SEARCH);
            i.putExtra(SearchManager.QUERY,search);
            startActivity(i);
        }catch(Exception e){
            e.printStackTrace();
            noapps(s);
        }
    }
    private void noapps(String s){
        try {
            Uri u = Uri.parse("https://www.google.com/search?q"+s);
            Intent i = new Intent(Intent.ACTION_SEARCH);
//            i.putExtra(SearchManager.QUERY,search);
            startActivity(i);
        }catch(Exception e){
            e.printStackTrace();
        }
    }


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        searchString = findViewById(R.id.searchText);
        searchBtn = findViewById(R.id.searchSubmit);

        searchBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                search = searchString.getText().toString();
                search(search);

            }
        });

    }
}