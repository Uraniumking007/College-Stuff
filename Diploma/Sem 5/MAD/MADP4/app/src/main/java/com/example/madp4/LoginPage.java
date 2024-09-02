package com.example.madp4;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.example.madp4.MainActivity;

public class LoginPage extends AppCompatActivity {

    static final String ValidUsername = "contact@bhaveshp.dev";
    static final String ValidPassword = "testing";

    public EditText username,password;
    public Button loginBtn;

    public void auth(String user, String pass){
        if (user.isEmpty()|| pass.isEmpty()){
            Toast.makeText(this, "Username & password are Required",Toast.LENGTH_SHORT).show();
        }
        if(user.equals(ValidUsername) && pass.equals(ValidPassword)){
            Toast.makeText(this,"Login Success", Toast.LENGTH_SHORT).show();

            Intent i = new Intent(LoginPage.this, MainActivity.class);
            i.putExtra("username",user);
            startActivity(i);
            finish();

        } else {
            Toast.makeText(this,"Username or password is Incorrect", Toast.LENGTH_SHORT).show();
        }
    }



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login_page);

        username = findViewById(R.id.loginUsername);
        password = findViewById(R.id.loginPassword);
        loginBtn = findViewById(R.id.loginSubmit);



        loginBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String user = username.getText().toString();
                String pass = password.getText().toString();

                auth(user,pass);


            }
        });

    }
}