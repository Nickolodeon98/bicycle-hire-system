package com.example.bottomnav;


import android.content.Context;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.SharedPreferences.Editor;
import android.widget.TextView;



/**
 * A simple {@link Fragment} subclass.
 */
public class Account extends Fragment {
    private TextView ac_username;
    private TextView ac_email;
    private String un,em;
    SharedPreferences sp;


    public Account() {
        // Required empty public constructor
    }


    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_account, container, false);
    }


    @Override
    public void onActivityCreated( Bundle savedInstanceState) {
        super.onActivityCreated(savedInstanceState);
        sp=getActivity().getSharedPreferences("user_data", Context.MODE_PRIVATE);
        ac_username= getActivity().findViewById(R.id.ac_username);
        ac_email= getActivity().findViewById(R.id.ac_email);
        un = sp.getString("name", "");
        em = sp.getString("email", "");
        ac_username.setText(un);
        ac_email.setText(em);
    }



}
