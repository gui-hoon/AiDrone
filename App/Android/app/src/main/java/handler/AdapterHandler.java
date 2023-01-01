package handler;

import android.app.Activity;
import android.os.Handler;
import android.os.Message;
import android.widget.TextView;

import androidx.annotation.NonNull;

import com.root.myapplication.R;

import adapters.LogAdapter;
import adapters.MyAdapter;
import manager.DataManager;
import manager.HandlerManager;

public class AdapterHandler extends Handler {

    MyAdapter adapter;
    LogAdapter logAdapter;

    public AdapterHandler(MyAdapter adapter)
    {
        this.adapter = adapter;
        this.logAdapter = null;
    }

    public void setLogAdapter(LogAdapter adapter)
    {
        this.logAdapter = adapter;
    }
    @Override
    public void handleMessage(@NonNull Message msg) {
        super.handleMessage(msg);

        adapter.update();

        if(logAdapter != null)
        {
            logAdapter.updateList();
            logAdapter.notifyDataSetChanged();
        }


        HandlerManager.getInstance().setRun(false);
    }
}
