package com.example.bottomnav;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.Looper;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.app.Activity;
import android.widget.TextView;
import android.widget.Toast;

import com.example.bottomnav.MainActivity;
import com.example.bottomnav.R;

import org.apache.http.util.EncodingUtils;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.io.InputStream;
import java.util.Date;


public class orders extends AppCompatActivity {
    private TextView order_info;

    @Override
    protected void onCreate( Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.order);

        Button settinghuitui= (Button) findViewById(R.id.settinghuitui);
        settinghuitui.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(orders.this, MainActivity.class);
                startActivity(intent);
            }
        });

        order_info=findViewById(R.id.order_info);
        showOrder();

    }

    private void showOrder(){
        final String urlStr="http://122.114.237.201/usercontrol/login";
        new Thread(){
            @Override
            public void run() {
                SharedPreferences sp=getSharedPreferences("user_data", MODE_PRIVATE);
                int user_id=sp.getInt("user_id", 0);
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
                    order_info.setText("");
                    JSONArray result_json=new JSONArray(result1);
                    int id=0;
                    for (int i = 0; i < result_json.length(); i++) {
                        try {
                            JSONObject object = result_json.getJSONObject(i);
                            int u_id=object.getInt("id");
                            if (u_id==user_id){
                                id=id+1;
                                String name=object.getString("name");
                                String author=object.getString("author");
                                double total=object.getDouble("price");
                                String orderinfo="Order number:  "+id
                                        +"\nUser name:  "+name
                                        +"\nAuthor:  "+author+
                                        "\n Total price:  "+total+"\n\n";
                                order_info.append(orderinfo);
                            }


                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }

                } catch (JSONException e) {
                    e.printStackTrace();
                    System.out.println(e.toString());
                }


            }
        }.start();
    }
}

