package com.example.bashabhara;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.app.DatePickerDialog;
import android.content.Intent;
import android.os.Bundle;
import android.text.TextUtils;
import android.util.Patterns;
import android.view.View;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.ProgressBar;
import android.widget.EditText;
import android.widget.Toast;

import java.util.Calendar;
import java.util.Date;


public class RegisterActivity extends AppCompatActivity {

    private EditText editTextRegisterFullName, editTextRegisterEmail, editTextRegisterDoB, editTextRegisterDoB, editTextRegisterMobile, editTextRegisterPwd, editTextRegisterConfirmPwd;
    private ProgressBar progressBar;
    private RadioGroup radioGroupRegisterGender;
    private RadioButton radioButtonRegisterGenderSelected;
    private DatePickerDialog picker;
    private static final String TAG = "RegisterActivity";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        getSupportActionBar().setTitle("Register");

        Toast.makeText(RegisterActivity.this, "You can register now", Toast.LENGTH_LONG).show();

        editTextRegisterFullName = findViewById((R.id.editText_register_full_name);
        editTextRegisterEmail = findViewById(R.id.editText_register_email);
        editTextRegisterDoB = findViewById(R.id.editText_register_dob);
        editTextRegisterMobile = findViewById(R.id.editText_register_mobile);
        editTextRegisterPwd = findViewById(R.id.editText_register_pwd);
        editTextRegisterConfirmPwd = findViewById(R.id.register_confirm_pwd);

        radioGroupRegisterGender = findViewById(R.id.radio_group_register_gender);
        radioGroupRegisterGender.clearCheck();

        editTextRegisterDoB.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v) {
                final Calendar calendar = Calendar.getInstance();
                int day = calendar.get(Calendar.DAY_OF_MONTH);
                int month = calendar.get(calendar.MONTH);
                int year = calendar.get(Calendar.YEAR);

                picker = new DatePickerDialog(RegisterActivity.this, new DatePickerDialog.OnDateSetListener(){
                    @Override
                    public void onDataSet(DatePicker view, int year, int month, int dayOfMonth){
                        editTextRegisterDoB.setText(dayOfMonth + "/" + (month+1) + "/" + year);

                    }

                }, year, month, day);
                picker.show();
            }
        });

        Button buttonRegister = findViewById(R.id.button_register);
        buttonRegister.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v){
                int selectGenderId = radioGroupRegisterGender.getCheckedRadioButtonId();
                radioButtonRegisterGenderSelected = findViewById(selectGenderId);

                String textFullName = editTextRegisterFullName.getText().toString();
                String textEmail = editTextRegisterEmail.getText().toString();
                String textDoB = editTextRegisterDoB.getText().toString();
                String textMobile = editTextRegisterMobile.getText().toString();
                String textPwd = editTextRegisterPwd.getText().toString();
                String textConfirmPwd = editTextRegisterConfirmPwd.getText().toString();
                String textGender;

                if(TextUtils.isEmpty(textFullName)){
                    Toast.makeText(RegisterActivity.this, "Please enter your full name",Toast.LENGTH_LONG).show();
                    editTextRegisterFullName.setError("Full Name is required");
                    editTextRegisterFullName.requestFocus();
                } else if (TextUtils.isEmpty(textEmail)) {
                    Toast.makeText(RegisterActivity.this, "Please enter your email",Toast.LENGTH_LONG).show();
                    editTextRegisterEmail.setError("Email is required");
                    editTextRegisterEmail.requestFocus();
                } else if(!Patterns.EMAIL_ADDRESS.matcher(textEmail).matches()) {
                    Toast.makeText(RegisterActivity.this, "PLease re-enter your email",Toast.LENGTH_LONG).show();
                    editTextRegisterEmail.setError("Valid email is required");
                    editTextRegisterEmail.requestFocus();
                } else if (TextUtils.isEmpty(textDoB)) {
                    Toast.makeText(RegisterActivity.this, "Please enter your date of birth",Toast.LENGTH_LONG).show();
                    editTextRegisterEmail.setError("Date of Birth is required");
                    editTextRegisterEmail.requestFocus();
                } else if (radioGroupRegisterGender.getCheckedRadioButtonId() == -1) {
                    Toast.makeText(RegisterActivity.this, "Please enter your gender",Toast.LENGTH_LONG).show();
                    editTextRegisterEmail.setError("Gender is required");
                    editTextRegisterEmail.requestFocus();
                } else if (TextUtils.isEmpty(textMobile)) {
                    Toast.makeText(RegisterActivity.this, "Please enter your mobile no.",Toast.LENGTH_LONG).show();
                    editTextRegisterEmail.setError("Mobile No. is required");
                    editTextRegisterEmail.requestFocus();
                } else if (textMobile.length() != 11) {
                    Toast.makeText(RegisterActivity.this, "Please re-enter your mobile no.",Toast.LENGTH_LONG).show();
                    editTextRegisterEmail.setError("Mobile No. should be 11 digits");
                    editTextRegisterEmail.requestFocus();
                } else if (TextUtils.isEmpty(textPwd)) {
                    Toast.makeText(RegisterActivity.this, "Please enter your password",Toast.LENGTH_LONG).show();
                    editTextRegisterEmail.setError("Password is required");
                    editTextRegisterEmail.requestFocus();
                } else if (textPwd.length() < 6) {
                    Toast.makeText(RegisterActivity.this, "Password should be at least 6 characters",Toast.LENGTH_LONG).show();
                    editTextRegisterEmail.setError("Password too weak");
                    editTextRegisterEmail.requestFocus();
                } else if (TextUtils.isEmpty(textConfirmPwd)) {
                    Toast.makeText(RegisterActivity.this, "Please confirm your password",Toast.LENGTH_LONG).show();
                    editTextRegisterEmail.setError("Password confirmation is required");
                    editTextRegisterEmail.requestFocus();
                } else if (!textPwd.equals(textConfirmPwd)) {
                    Toast.makeText(RegisterActivity.this, "Please enter the same password",Toast.LENGTH_LONG).show();
                    editTextRegisterEmail.setError("Password must match");
                    editTextRegisterEmail.requestFocus();
                    editTextRegisterPwd.clearComposingText();
                    editTextRegisterConfirmPwd.clearComposingText();
                } else {
                    textGender = radioButtonRegisterGenderSelected.getText().toString();
                    progressBar.setVisibility(View.VISIBLE);
                    registerUser(textFullName, textEmail, textDoB, textGender, textMobile, textPwd);
                }
            }
        });
    }

    private void registerUser(final String textFullName, String textEmail, final String textDoB, final String textGender, final String textMobile, String textPwd) {
        FirebaseAuth auth = FirebaseAuth.getInstance;
        auth.createUserWithEmailAndPassword(textEmail, textPwd).addonCompleteListener(RegisterActivity.this,
                new OnCompleteListener<AuthResult>(){
                    @Override
                    public void onComplete(@NonNull Task<AuthResult> task) {
                        if (task.isSuccessful()){
                            Toast.makeText(RegisterActivity.this, "User Registered Successfully",Toast.LENGTH_LONG).show();
                            FirebaseUser firebaseUser = auth.getCurrentUser();

                            UserProfileChangeRequest = new UserProfileChangeRequest.Builder().setDisplayName(textFullName).build();
                            firebaseUser.updateProfile(profileChangeRequest);

                            ReadWriteUserDetails writeUserDetails = new ReadWriteUserDetails(textDoB, textGender, textMobile);

                            DatabaseReference referenceProfile = FirebaseDatabase.getInstance().getReference("Registered Users");

                            referenceProfile.child(FirebaseUser.getUid()).setvalue(writeUserDetails).addOnCompleteListener(new OnCompleteListener<Void>{
                                @Override
                                public void onComplete(@NonNull Task<Void> task) {
                                    firebaseUser.sendEmailVerification();

                                    Toast.makeText(RegisterActivity.this, "User Registered Successfully. Please Verify Email.",Toast.LENGTH_LONG).show();

                                    Intent intent = new Intent(RegisterActivity.this,UserProfileActivity.class);
                                    intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_CLEAR_TASK | Intent.FLAG_ACTIVITY_NEW_TASK);
                                    startActivity(intent);
                                    finish();
                                }
                            } else {
                                Toast.makeText(RegisterActivity.this, "User Registration failed. Please trt again.",Toast.LENGTH_LONG).show();
                                progressBar.setVisibility(View.GONE);
                            }
                        }
                    }
                }
    }
}
