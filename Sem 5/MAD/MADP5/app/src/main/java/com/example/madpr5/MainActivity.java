package com.example.madpr5;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.Manifest;
import android.app.SearchManager;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Bundle;
import android.telephony.SmsManager;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    EditText searchString, phoneNumber,recieverNo,messageContent;
    Button searchBtn, callBtn,sendSMS ;

    public String search, phoneNumberr, recievernumber,msgContent ;


    public void search(String search) {
        if (search.isEmpty()) {
            Toast.makeText(this, "Username & password are Required", Toast.LENGTH_SHORT).show();
        } else {
            defaultBrowser(search);
            noapps(search);
        }
    }

    private void defaultBrowser(String s) {
        try {
            Intent i = new Intent(Intent.ACTION_WEB_SEARCH);
            i.putExtra(SearchManager.QUERY, search);
            startActivity(i);
        } catch (Exception e) {
            e.printStackTrace();
            noapps(s);
        }
    }

    private void noapps(String s) {
        try {
            Uri u = Uri.parse("https://www.google.com/search?q=" + s);
            Intent i = new Intent(Intent.ACTION_SEARCH);
//            i.putExtra(SearchManager.QUERY,search);
            startActivity(i);
        } catch (Exception e) {
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
        sendSMS = findViewById(R.id.sendSMS);
        recieverNo = findViewById(R.id.recieverNo);
        messageContent = findViewById(R.id.messageContent);

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
                if (ContextCompat.checkSelfPermission(MainActivity.this, android.Manifest.permission.CALL_PHONE) == PackageManager.PERMISSION_GRANTED) {
                    makephonecall();
                } else {
                    ActivityCompat.requestPermissions(MainActivity.this, new String[]{Manifest.permission.CALL_PHONE}, 100);
                }
            }
        });
        sendSMS.setOnClickListener(view -> {
            if(ContextCompat.checkSelfPermission(MainActivity.this, Manifest.permission.SEND_SMS)== PackageManager.PERMISSION_GRANTED){
                sendMessage();
            } else {
                ActivityCompat.requestPermissions(MainActivity.this,new String[]{Manifest.permission.SEND_SMS},101);
            }
        });

    }

    private void sendMessage() {
        recievernumber = recieverNo.getText().toString();
        msgContent = messageContent.getText().toString();
        if(recievernumber.isEmpty() && msgContent.isEmpty() ){
            Toast.makeText(this, "Enter Valid Phone and message", Toast.LENGTH_SHORT).show();
            return;
        }
        if(recievernumber.isEmpty()){
            Toast.makeText(this, "Enter Phone Number", Toast.LENGTH_SHORT).show();
            return;
        }
        if(msgContent.isEmpty()){
            Toast.makeText(this, "Enter Message", Toast.LENGTH_SHORT).show();
            return;
        }
        Intent i = new Intent(Intent.ACTION_SEND);
        SmsManager smsManager = SmsManager.getDefault();
        smsManager.sendTextMessage(recievernumber,null,msgContent,null,null);
        Toast.makeText(this, "Message Sent", Toast.LENGTH_SHORT).show();
    }


    public void makephonecall() {
        phoneNumberr = phoneNumber.getText().toString();
        if (phoneNumberr.length() > 10 || phoneNumberr.length() < 10) {
            Toast.makeText(MainActivity.this, "Enter A Valid Phone Number", Toast.LENGTH_SHORT).show();
        } else {
            Intent makeCall = new Intent(Intent.ACTION_CALL);
            makeCall.setData(Uri.parse("tel:" + phoneNumberr));
            startActivity(makeCall);
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == 100) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                makephonecall();
            } else {
                Toast.makeText(this, "Permission Denied", Toast.LENGTH_SHORT).show();
            }
        }
        if(requestCode == 101){
            if(grantResults.length>0 && grantResults[0] == PackageManager.PERMISSION_GRANTED){
                sendMessage();
            }
        }
    }

}