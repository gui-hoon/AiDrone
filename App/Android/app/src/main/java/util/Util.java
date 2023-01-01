package util;

import android.os.Bundle;
import android.os.Message;

import com.root.myapplication.R;

public class Util {
    static public Message getMessage(String key, int value)
    {
        Message msg = new Message();
        Bundle bundle = new Bundle();

        bundle.putInt(key, value);
        msg.setData(bundle);

        return msg;
    }

    static public Message getMessage(String key, boolean value)
    {
        Message msg = new Message();
        Bundle bundle = new Bundle();

        bundle.putBoolean(key, value);
        msg.setData(bundle);

        return msg;
    }

    static public int getColorFromType(State.Type type)
    {
        int output = 0;

        if(type == State.Type.NOT_FILL)
            output = R.color.red;
        else if(type == State.Type.FILLING_MINE || type == State.Type.FILLING)
            output = R.color.yellow;
        else if(type == State.Type.FINISHED)
            output = R.color.green;

        return output;
    }
}
