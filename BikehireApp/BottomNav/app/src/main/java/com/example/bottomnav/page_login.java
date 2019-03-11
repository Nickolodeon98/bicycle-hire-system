package com.example.bottomnav;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.Looper;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.example.bottomnav.MainActivity;
import com.example.bottomnav.R;
import com.example.bottomnav.internet.internet;

import org.json.JSONObject;
import org.json.JSONArray;
import java.util.ArrayList;
import org.apache.http.util.EncodingUtils;
import org.json.JSONException;


import java.io.IOException;
import java.io.InputStream;


public class page_login extends AppCompatActivity {

    private TextView tv_lgi_hop;
    private TextView username;
    private TextView password;
    private Button log_button;
    int flag;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.page_login);
        final Intent intent=getIntent();
        flag=intent.getIntExtra("flag",0);
        tv_lgi_hop=(TextView) findViewById(R.id.lgi_tv_hop);
        username=(TextView) findViewById(R.id.username);
        password=(TextView) findViewById(R.id.lgi_et_psw);
        log_button=(Button) findViewById(R.id.lgi_bt_lgi);
        tv_lgi_hop.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                    Intent intent1=new Intent(page_login.this, MainActivity.class);
                    startActivity(intent1);

                finish();
            }
        });



        /**
         *
         */
        log_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                final String urlStr="http://122.114.237.201/usercontrol/login";
                final String num=username.getText().toString().trim();
                final String psw=password.getText().toString().trim();

                if("".equals(num)||"".equals(psw))
                {
                    Toast.makeText(page_login.this,"Please enter the right username and password",Toast.LENGTH_SHORT).show();
                }
                else
                {
                    new Thread(){
                        @Override
                        public void run() {
                            int check = 0;
                            int id=0;
                            String name="";
                            String email="";
                            String password="";
                            //String result= internet.gethttpresult(urlStr);
                            String result1="";
                            String result="";
                            try {


                                InputStream is = getResources().getAssets().open("test.json");
                                int length = is.available();
                                byte[] buffer = new byte[length];
                                is.read(buffer);
                                result = EncodingUtils.getString(buffer, "utf-8");
                                is.close();

                            } catch (IOException e){
                                e.printStackTrace();
                            }
                            result1=result.substring(result.indexOf("["),result.indexOf("]")+1);

                            try {
                                JSONArray result_json=new JSONArray(result1);

                                for (int i = 0; i < result_json.length(); i++) {
                                    try {
                                        JSONObject object = result_json.getJSONObject(i);
                                        id = object.getInt("id");
                                        name = object.getString("name");
                                        email = object.getString("press");
                                        password = object.getString("author");

                                        if (num.equals(name) && psw.equals(password)) {
                                            check = 1;
                                            break;
                                        }
                                    } catch (JSONException e) {
                                        e.printStackTrace();
                                    }
                                }

                                if(check==1)
                                    {
                                        SharedPreferences user_data=getSharedPreferences("user_data",MODE_PRIVATE);
                                        SharedPreferences.Editor et=user_data.edit();
                                        et.putInt("user_id",id);
                                        et.putString("name", name);
                                        et.putString("email", email);
                                        et.putString("password", password);
                                        et.commit();

                                        Intent intent1=new Intent(page_login.this,MainActivity.class);
                                        startActivity(intent1);

                                        finish();
                                    }
                                if(check==0)
                                {
                                    Looper.prepare();
                                    Toast.makeText(page_login.this,"Please enter the right username and password",Toast.LENGTH_SHORT).show();
                                    Looper.loop();
                                }


                                } catch (JSONException e) {
                                    e.printStackTrace();
                                    System.out.println(e.toString());
                                }


                        }
                    }.start();
                }
            }
        });
    }
}
