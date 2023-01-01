package activity;

import android.os.Bundle;
import android.view.View;
import android.widget.CheckBox;
import android.widget.CompoundButton;
import android.widget.GridView;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import com.root.myapplication.R;

import adapters.LogAdapter;
import handler.AdapterHandler;
import manager.HandlerManager;

public class LogActivity extends AppCompatActivity {

    CheckBox red, yellow, green;
    GridView gridView;
    LogAdapter adapter;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.log_activity);

        red = findViewById(R.id.cb_log_red);
        yellow = findViewById(R.id.cb_log_yellow);
        green = findViewById(R.id.cb_log_green);

        red.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                adapter.updateList();
                adapter.notifyDataSetChanged();
            }
        });
        yellow.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                adapter.updateList();
                adapter.notifyDataSetChanged();
            }
        });
        green.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                adapter.updateList();
                adapter.notifyDataSetChanged();
            }
        });
        red.setChecked(true);
        yellow.setChecked(true);
        green.setChecked(true);

        gridView = findViewById(R.id.gridview_log);
        adapter = new LogAdapter(this, this, red, yellow, green);

        ((AdapterHandler)HandlerManager.getInstance().getHandler("AdapterHandler")).setLogAdapter(adapter);

        gridView.setAdapter(adapter);
    }
}
