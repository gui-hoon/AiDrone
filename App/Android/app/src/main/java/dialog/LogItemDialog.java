package dialog;

import android.app.Activity;
import android.app.Dialog;
import android.content.Context;
import android.graphics.Point;
import android.os.Message;
import android.view.Display;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.ImageView;

import androidx.constraintlayout.widget.ConstraintLayout;

import com.root.myapplication.R;

import adapters.LogAdapter;
import manager.DataManager;
import manager.HandlerManager;
import manager.NetworkManager;
import util.Network;
import util.State;
import util.Util;

public class LogItemDialog extends Dialog {

    Button ok_btn, finish_btn, cancel_btn;
    ImageView imageView;
    ConstraintLayout layout, notfillLayout, fillingLayout, finishLaoyut;
    String imageName;
    Context context;
    Activity activity;

    public LogItemDialog(Context context, Activity activity)
    {
        super(context);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        setContentView(R.layout.log_item_dialog);

        this.context = context;
        this.activity = activity;

        setWindowSize();

        ok_btn = findViewById(R.id.log_yes_button);
        finish_btn = findViewById(R.id.log_finish_btn);
        cancel_btn = findViewById(R.id.log_cancel_btn);
        layout = findViewById(R.id.log_item_dialog_background);
        notfillLayout = findViewById(R.id.log_state_not_fill_layout);
        fillingLayout = findViewById(R.id.log_state_filling_layout);
        finishLaoyut = findViewById(R.id.log_state_finish_layout);
        imageView = findViewById(R.id.iv_log_dialog);

        ok_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                DataManager.getinstance().setState(imageName, State.Type.FILLING_MINE);
                NetworkManager.getInstance().send(Network.IMG_STATE + imageName + " : " + State.getTypeToInt(State.Type.FILLING));
                changeLayout(DataManager.getinstance().getState(imageName));
                layout.setBackgroundColor(context.getResources().getColor(Util.getColorFromType(DataManager.getinstance().getState(imageName))));
            }
        });

        finish_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                DataManager.getinstance().setState(imageName, State.Type.FINISHED);
                NetworkManager.getInstance().send(Network.IMG_STATE + imageName + " : " + State.getTypeToInt(State.Type.FINISHED));
                changeLayout(DataManager.getinstance().getState(imageName));
                layout.setBackgroundColor(context.getResources().getColor(Util.getColorFromType(DataManager.getinstance().getState(imageName))));
            }
        });

        cancel_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                DataManager.getinstance().setState(imageName, State.Type.NOT_FILL);
                NetworkManager.getInstance().send(Network.IMG_STATE + imageName + " : " + State.getTypeToInt(State.Type.NOT_FILL));
                changeLayout(DataManager.getinstance().getState(imageName));
                layout.setBackgroundColor(context.getResources().getColor(Util.getColorFromType(DataManager.getinstance().getState(imageName))));
            }
        });
    }

    public void show(String imageName)
    {
        this.imageName = imageName;

        State.Type type = DataManager.getinstance().getState(this.imageName);
        layout.setBackgroundColor(context.getResources().getColor(Util.getColorFromType(type)));

        imageView.setImageBitmap(DataManager.getinstance().getImage(imageName));

        changeLayout(type);

        show();
    }

    private void resetLayout()
    {
        notfillLayout.setVisibility(View.GONE);
        fillingLayout.setVisibility(View.GONE);
        finishLaoyut.setVisibility(View.GONE);
    }

    private void changeLayout(State.Type type)
    {
        resetLayout();

        if(type == State.Type.NOT_FILL)
            notfillLayout.setVisibility(View.VISIBLE);
        else if(type == State.Type.FILLING)
            fillingLayout.setVisibility(View.VISIBLE);
        else if(type == State.Type.FILLING_MINE)
            finishLaoyut.setVisibility(View.VISIBLE);
    }

    private void setWindowSize()
    {
        Display display = activity.getWindowManager().getDefaultDisplay();
        Point size = new Point();
        display.getRealSize(size);

        WindowManager.LayoutParams lp = getWindow().getAttributes();
        lp.width = size.x / 10 * 7;
        lp.height = WindowManager.LayoutParams.WRAP_CONTENT;
        getWindow().setAttributes(lp);
    }


}