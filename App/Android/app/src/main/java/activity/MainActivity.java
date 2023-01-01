package activity;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.AppCompatButton;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.PagerSnapHelper;
import androidx.recyclerview.widget.RecyclerView;
import androidx.recyclerview.widget.SnapHelper;

import android.content.Intent;
import android.os.Bundle;
import android.os.Message;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.root.myapplication.R;

import java.util.List;

import adapters.MyAdapter;
import handler.AdapterHandler;
import handler.CountHandler;
import handler.StateHandler;
import manager.DataManager;
import manager.HandlerManager;
import manager.NetworkManager;
import util.Network;
import util.State;
import util.Util;

public class MainActivity extends AppCompatActivity {

    private long backKeyPressedTime = 0;

    private ImageView drone_state_iv;
    private Button OK_iv, finish_iv, cancel_iv, streaming_btn;
    private TextView count_tv;
    private RecyclerView recyclerView;
    private MyAdapter adapter;
    private SnapHelper snapHelper;
    LinearLayoutManager layoutManager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main_activity);

        count_tv = findViewById(R.id.tv_image_count);
        OK_iv = findViewById(R.id.yes_button);
        finish_iv = findViewById(R.id.finish_btn);
        cancel_iv = findViewById(R.id.cancel_btn);
        streaming_btn = findViewById(R.id.btn_streaming);

        drone_state_iv = findViewById(R.id.iv_drone_state);

        drone_state_iv.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(MainActivity.this, LogActivity.class);

                startActivity(intent);
            }
        });

        streaming_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(MainActivity.this, StreamingActivity.class);

                startActivity(intent);
            }
        });

        OK_iv.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                int pos = getPosFromTextView();
                String imageName = DataManager.getinstance().getKeyNotFinishDataFromPosition(pos);

                DataManager.getinstance().setState(imageName, State.Type.FILLING_MINE);
                NetworkManager.getInstance().send(Network.CreateSendMessage(NetworkManager.getInstance().getId(), Network.IMG_STATE,
                        imageName + "_" + State.getTypeToInt(State.Type.FILLING)));

                HandlerManager.getInstance().offer("StateHandler", Util.getMessage("state", State.getTypeToInt(DataManager.getinstance().getState(imageName))));
            }
        });

        finish_iv.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                int pos = getPosFromTextView();
                String imageName = DataManager.getinstance().getKeyNotFinishDataFromPosition(pos);

                DataManager.getinstance().setState(imageName, State.Type.FINISHED);
                NetworkManager.getInstance().send(Network.CreateSendMessage(NetworkManager.getInstance().getId(), Network.IMG_STATE,
                        imageName + "_" + State.getTypeToInt(State.Type.FINISHED)));

                adapter.update();
                String newImageName = DataManager.getinstance().getKeyNotFinishDataFromPosition(pos); // 전 이미지로 이동

                if(!newImageName.equals(""))
                {
                    HandlerManager.getInstance().offer("StateHandler", Util.getMessage("state", State.getTypeToInt(DataManager.getinstance().getState(newImageName))));
                    HandlerManager.getInstance().offer("CountHandler", Util.getMessage("pos", DataManager.getinstance().getPosFromImageName(newImageName) + 1));
                }
                else
                {
                    HandlerManager.getInstance().offer("StateHandler", new Message());
                    HandlerManager.getInstance().offer("CountHandler", new Message());
                }
            }
        });

        cancel_iv.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                int pos = getPosFromTextView();
                String imageName = DataManager.getinstance().getKeyNotFinishDataFromPosition(pos);

                DataManager.getinstance().setState(imageName, State.Type.NOT_FILL);
                NetworkManager.getInstance().send(Network.CreateSendMessage(NetworkManager.getInstance().getId(), Network.IMG_STATE,
                        imageName + "_" + State.getTypeToInt(State.Type.NOT_FILL)));

                HandlerManager.getInstance().offer("StateHandler", Util.getMessage("state", State.getTypeToInt(DataManager.getinstance().getState(imageName))));
            }
        });

        adapter = new MyAdapter(this, this);
        layoutManager = new LinearLayoutManager(this, LinearLayoutManager.HORIZONTAL, false);

        recyclerView = findViewById(R.id.recycler_view);
        recyclerView.setAdapter(adapter);
        recyclerView.setLayoutManager(layoutManager);

        snapHelper = new PagerSnapHelper();
        snapHelper.attachToRecyclerView(recyclerView);

        HandlerManager.getInstance().putHandler("StateHandler", new StateHandler(this));
        HandlerManager.getInstance().putHandler("AdapterHandler", new AdapterHandler(adapter));
        HandlerManager.getInstance().putHandler("CountHandler", new CountHandler(this));

        recyclerView.addOnScrollListener(new RecyclerView.OnScrollListener() {
            @Override
            public void onScrollStateChanged(RecyclerView recyclerView, int newState) {
                super.onScrollStateChanged(recyclerView, newState);
                if(newState == RecyclerView.SCROLL_STATE_IDLE) {

                    if(DataManager.getinstance().getSize() <= 1)
                        return;

                    View centerView = snapHelper.findSnapView(layoutManager);
                    int pos = layoutManager.getPosition(centerView);

                    String currentView = DataManager.getinstance().getKeyNotFinishDataFromPosition(pos);
                    State.Type type = DataManager.getinstance().getState(currentView);

                    HandlerManager.getInstance().offer("StateHandler", Util.getMessage("state", State.getTypeToInt(type)));
                    HandlerManager.getInstance().offer("CountHandler", Util.getMessage("pos", pos + 1));
                }
            }
        });

    }

    @Override
    protected void onStart() {
        super.onStart();

        int pos = getPosFromTextView();

        adapter.update();
        String newImageName = DataManager.getinstance().getKeyNotFinishDataFromPosition(pos);

        if(!newImageName.equals(""))
        {
            HandlerManager.getInstance().offer("StateHandler", Util.getMessage("state", State.getTypeToInt(DataManager.getinstance().getState(newImageName))));
            HandlerManager.getInstance().offer("CountHandler", Util.getMessage("pos", DataManager.getinstance().getPosFromImageName(newImageName) + 1));
        }
        else
        {
            HandlerManager.getInstance().offer("StateHandler", new Message());
            HandlerManager.getInstance().offer("CountHandler", new Message());
        }
    }

    @Override
    public void onBackPressed() {
        if(System.currentTimeMillis() > backKeyPressedTime + 2000)
        {
            backKeyPressedTime = System.currentTimeMillis();
            Toast.makeText(this, "뒤로가기 버튼을 두번 누르시면 종료됩니다.", Toast.LENGTH_SHORT).show();
            return;
        }

        if(System.currentTimeMillis() <= backKeyPressedTime + 2000)
        {
            moveTaskToBack(true);
            finishAndRemoveTask();
            android.os.Process.killProcess(android.os.Process.myPid());
        }
    }

    private int getPosFromTextView()
    {
        String text = count_tv.getText().toString();
        return Integer.parseInt(text.split(" / ")[0]) - 1;
    }
}