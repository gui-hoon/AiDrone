package handler;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.view.View;
import android.widget.ImageView;

import androidx.annotation.NonNull;
import androidx.constraintlayout.widget.ConstraintLayout;

import com.root.myapplication.R;

import activity.MainActivity;
import manager.HandlerManager;
import manager.NetworkManager;

public class ConnectHandler extends Handler {

    ConstraintLayout layout;
    ImageView imageView;
    Activity activity;
    Context context;

    public ConnectHandler(Activity activity, Context context)
    {
        this.activity = activity;
        this.context = context;

        layout = activity.findViewById(R.id.connection_layout);
        imageView = activity.findViewById(R.id.btn_connection);
        layout.setVisibility(View.INVISIBLE);

        imageView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                layout.setVisibility(View.INVISIBLE);
                NetworkManager.getInstance().tryConnect(context);
            }
        });

    }


    @Override
    public void handleMessage(@NonNull Message msg) {
        super.handleMessage(msg);

        Bundle bundle = msg.getData();
        boolean value = bundle.getBoolean("value");
        if(value)
        {
            Intent intent = new Intent(context, MainActivity.class);

            activity.startActivity(intent);
        }
        else
        {
            layout.setVisibility(View.VISIBLE);
        }

        HandlerManager.getInstance().setRun(false);
    }
}
