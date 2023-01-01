package activity;

import android.os.Bundle;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.widget.ImageView;

import androidx.appcompat.app.AppCompatActivity;
import androidx.constraintlayout.widget.ConstraintLayout;

import com.root.myapplication.R;

import handler.ConnectHandler;
import manager.HandlerManager;
import manager.NetworkManager;

public class LodingActivity extends AppCompatActivity {

    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.loading_activity);

        HandlerManager.getInstance().putHandler("ConnectHandler", new ConnectHandler(this, this));

        NetworkManager.Create();
        NetworkManager.getInstance().tryConnect(this);
    }

    @Override
    protected void onResume() {
        super.onResume();

    }
}
