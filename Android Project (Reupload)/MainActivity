package com.example.bashabhara;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        getSupportActionBar().setTitle("BashaBhara");

                Button buttonLogin = findViewById(R.id.button_login);
                buttonLogin.setOnClickListener(new View.OnClickListener(){
                    @Override
                    public void onClick(View v) {
                        Intent intent = new Intent( packageContext: MainActivity.this, LoginActivity.class);
                        startActivity(intent);
                    }
                });

                Button buttonRegister = findViewById(R.id.button_login);
                buttonRegister.setOnClickListener(new View.OnClickListener(){
                    @Override
                    public void onClick(View v) {
                        Intent intent = new Intent( packageContext: MainActivity.this, RegisterActivity.class);
                        startActivity(intent);
                    }
                });




    }
}

