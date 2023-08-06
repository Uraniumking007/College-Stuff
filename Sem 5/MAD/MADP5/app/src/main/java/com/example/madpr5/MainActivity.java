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

    EditText searchString, phoneNumber;
    Button searchBtn, callBtn;

    public String search,phoneNumberr;


    public void search(String search){
        if(search.isEmpty()){
            Toast.makeText(this, "Username & password are Required",Toast.LENGTH_SHORT).show();
        }else {
            defaultBrowser(search);
            noapps(search);
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
        phoneNumber = findViewById(R.id.phoneNumber);
        callBtn = findViewById(R.id.makeCall);

        searchBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                search = searchString.getText().toString();
                search(search);

            }
        });

        callBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                phoneNumberr = phoneNumber.getText().toString();
                if(phoneNumberr.length() > 10 || phoneNumberr.length() < 10){
                    Toast.makeText(MainActivity.this, "Enter A Valid Phone Number", Toast.LENGTH_SHORT).show();
                } else {
                    Intent makeCall = new Intent(Intent.ACTION_CALL);
                    makeCall.setData(Uri.parse("tel:" + phoneNumberr));
                    startActivity(makeCall);
                }
            }
        });

    }
}