package com.example.bottomnav;

import android.support.annotation.NonNull;
import android.support.design.internal.BottomNavigationItemView;
import android.support.design.widget.BottomNavigationView;
import android.support.v4.app.Fragment;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.MenuItem;

public class MainActivity extends AppCompatActivity implements  BottomNavigationView.OnNavigationItemSelectedListener{
    private static final String TAG = "MainActivity";
    BottomNavigationView bottomNavigationView;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        bottomNavigationView = findViewById(R.id.bottom_nav_view);

        bottomNavigationView.setSelectedItemId(R.id.navigation_home);

        bottomNavigationView.setOnNavigationItemSelectedListener(this);
    }

    Home homeFragment = new Home();
    Location locationFragment = new Location();
    Account accountFragment = new Account();


    @Override
    public boolean onNavigationItemSelected(@NonNull MenuItem menuItem) {

        switch(menuItem.getItemId()){
            case R.id.navigation_home:
                getSupportFragmentManager().beginTransaction().setCustomAnimations(R.anim.fade_in, R.anim.fade_out).replace(R.id.container, homeFragment).commit();
                return true;
            case R.id.navigation_map:
                getSupportFragmentManager().beginTransaction().replace(R.id.container, locationFragment).commit();
                return true;
            case R.id.navigation_account:
                getSupportFragmentManager().beginTransaction().setCustomAnimations(R.anim.fade_in, R.anim.fade_out).replace(R.id.container, accountFragment).commit();
                return true;
        }

        return false;
    }
}
