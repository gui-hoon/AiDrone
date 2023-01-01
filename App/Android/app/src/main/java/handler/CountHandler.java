package handler;

import android.app.Activity;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.util.Log;
import android.widget.TextView;

import androidx.annotation.NonNull;

import com.root.myapplication.R;

import manager.DataManager;
import manager.HandlerManager;
import util.State;
import util.Util;

public class CountHandler extends Handler {

    TextView textView;

    public CountHandler(Activity activity)
    {
        textView = activity.findViewById(R.id.tv_image_count);
    }


    @Override
    public void handleMessage(@NonNull Message msg) {
        super.handleMessage(msg);

        Bundle bundle = msg.getData();
        int pos = bundle.getInt("pos", -1);

        int listSize = DataManager.getinstance().getSizeNotFinishList();


        if(pos == -1 &&  listSize > 0)
        {
            pos = Integer.parseInt(getCurrentPos(textView.getText().toString()));
            if(pos == 0)
                pos = 1;
        }
        else if(pos == -1 && listSize == 0)
            pos = 0;

        String imageName = DataManager.getinstance().getKeyNotFinishDataFromPosition(pos - 1);
        HandlerManager.getInstance().offer("StateHandler", Util.getMessage("state", State.getTypeToInt(DataManager.getinstance().getState(imageName))));

        textView.setText(pos + " / " + DataManager.getinstance().getSizeNotFinishList());

        HandlerManager.getInstance().setRun(false);
    }

    private String getCurrentPos(String pos)
    {
        String[] split = pos.split(" / ");
        return split[0];
    }


}
