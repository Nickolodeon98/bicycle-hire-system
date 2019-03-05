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

import org.json.JSONException;
import org.json.JSONObject;

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
                flag=2;
                if(flag==2){
                    Intent intent1=new Intent(page_login.this, MainActivity.class);
                    startActivity(intent1);
                }
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
                            String result= internet.checkuser(urlStr,num,psw);
                            System.out.println(result);
                            if (result.equals("not exsits"))
                            {
                                Looper.prepare();
                                Toast.makeText(page_login.this,"用户名不存在！",Toast.LENGTH_SHORT).show();
                                Looper.loop();
                            }
                            else if(result.equals("internet errar"))
                            {
                                Looper.prepare();
                                Toast.makeText(page_login.this,"网络连接错误！",Toast.LENGTH_SHORT).show();
                                Looper.loop();
                            }
                            else{
                                try {
                                    JSONObject result_json=new JSONObject(result);
                                    String message=result_json.getString("message:");
                                    if("success".equals(message))
                                    {
                                        SharedPreferences user_data=getSharedPreferences("user_data",MODE_PRIVATE);
                                        SharedPreferences.Editor et=user_data.edit();
                                        et.putInt("user_id",result_json.getInt("userID"));
                                        et.commit();
                                        if(flag==2){
                                            Intent intent1=new Intent(page_login.this,MainActivity.class);
                                            startActivity(intent1);
                                        }
                                        finish();
                                    }
                                    else
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

                        }
                    }.start();
                }
            }
        });
    }
}
