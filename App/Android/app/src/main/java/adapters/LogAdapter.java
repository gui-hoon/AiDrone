package adapters;

import android.app.Activity;
import android.content.Context;
import android.content.DialogInterface;
import android.graphics.Color;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.CheckBox;
import android.widget.ImageView;

import androidx.annotation.ColorInt;
import androidx.constraintlayout.widget.ConstraintLayout;

import com.root.myapplication.R;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import dialog.LogItemDialog;
import manager.DataManager;
import util.State;
import util.Util;

public class LogAdapter extends BaseAdapter {

    private CheckBox red, yellow, green;
    List<String> keys;
    LogItemDialog dialog;

    public LogAdapter(Context context, Activity activity, CheckBox red, CheckBox yellow, CheckBox green) {
        this.red = red;
        this.yellow = yellow;
        this.green = green;
        keys = getList();
        dialog = new LogItemDialog(context, activity);

        dialog.setOnDismissListener(new DialogInterface.OnDismissListener() {
            @Override
            public void onDismiss(DialogInterface dialog) {
                updateList();
                notifyDataSetChanged();
            }
        });

    }

    @Override
    public int getCount() {
        return keys.size();
    }

    @Override
    public Object getItem(int position) {
        return keys.get(position);
    }

    @Override
    public long getItemId(int position) {
        return position;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        Context context = parent.getContext();

        LayoutInflater inflater = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        convertView = inflater.inflate(R.layout.log_item, parent, false);

        ConstraintLayout layout = convertView.findViewById(R.id.log_item_background);
        layout.setBackgroundColor(context.getResources().getColor(Util.getColorFromType(DataManager.getinstance().getState(keys.get(position)))));

        ImageView imageView = convertView.findViewById(R.id.iv_log_item);
        imageView.setImageBitmap(DataManager.getinstance().getImage(keys.get(position)));

        final String imageName = keys.get(position);

        imageView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                dialog.show(imageName);
            }
        });


        return convertView;
    }

    public void updateList()
    {
        keys = getList();
    }

    private List<String> getList()
    {
        List<String> output = new ArrayList<>();
        List<String> keys = DataManager.getinstance().getKeys();

        for(String key : keys)
        {
            State.Type state = DataManager.getinstance().getState(key);

            if(red.isChecked() && state == State.Type.NOT_FILL)
                output.add(key);
            else if(yellow.isChecked() && (state == State.Type.FILLING || state == State.Type.FILLING_MINE))
                output.add(key);
            else if(green.isChecked() && state == State.Type.FINISHED)
                output.add(key);
        }

        return output;
    }
}
