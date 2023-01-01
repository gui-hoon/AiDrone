package handler;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.constraintlayout.widget.ConstraintLayout;

import com.root.myapplication.R;

import activity.MainActivity;
import adapters.MyAdapter;
import manager.DataManager;
import manager.HandlerManager;
import util.State;

public class StateHandler extends Handler {

    ConstraintLayout notfillLayout, fillingLayout, finishLayout, noimageLayout;
    ImageView imageView;
    Activity activity;

    public StateHandler(Activity activity)
    {
        notfillLayout = activity.findViewById(R.id.state_not_fill_layout);
        fillingLayout = activity.findViewById(R.id.state_filling_layout);
        finishLayout = activity.findViewById(R.id.state_finish_layout);
        noimageLayout = activity.findViewById(R.id.no_image_layout);
        imageView = activity.findViewById(R.id.iv_drone_state);

        this.activity = activity;
    }


    @Override
    public void handleMessage(@NonNull Message msg) {
        super.handleMessage(msg);

        Bundle bundle = msg.getData();
        int value = bundle.getInt("state", State.getTypeToInt(State.Type.NONE));
        State.Type type = State.Type.NONE;
        if(value >= 0)
             type = State.getType(value);

        resetlayout();

        int color = R.color.black;


        if(type == State.Type.NOT_FILL)
        {
            color = R.color.red;
            notfillLayout.setVisibility(View.VISIBLE);
        }
        else if(type == State.Type.FILLING)
        {
            color = R.color.yellow;
            fillingLayout.setVisibility(View.VISIBLE);
        }
        else if(type == State.Type.FILLING_MINE)
        {
            color = R.color.yellow;
            finishLayout.setVisibility(View.VISIBLE);
        }
        else if(type == State.Type.FINISHED)
        {
            color = R.color.green;
        }
        else if(type == State.Type.NONE)
        {
            noimageLayout.setVisibility(View.VISIBLE);
        }

        imageView.setColorFilter(activity.getColor(color));

        HandlerManager.getInstance().setRun(false);
    }

    private void resetlayout()
    {
        noimageLayout.setVisibility(View.GONE);
        notfillLayout.setVisibility(View.GONE);
        fillingLayout.setVisibility(View.GONE);
        finishLayout.setVisibility(View.GONE);
    }
}
