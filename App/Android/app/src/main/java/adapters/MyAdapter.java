package adapters;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.media.Image;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Adapter;
import android.widget.Button;
import android.widget.ImageView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.root.myapplication.R;

import java.util.ArrayList;
import java.util.List;

import activity.LogActivity;
import activity.MainActivity;
import activity.StreamingActivity;
import manager.DataManager;
import util.State;

//TODO : 테스트 매니저 데이터매니저로 바꾸기

public class MyAdapter extends RecyclerView.Adapter<MyAdapter.MyViewHolder> {

    Context context;
    Activity activity;

    public MyAdapter(Context context, Activity activity)
    {
        this.activity = activity;
        this.context = context;
    }


    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        LayoutInflater inflater = LayoutInflater.from(parent.getContext());
        View view = inflater.inflate(R.layout.view_holder_item, parent, false);

        ImageView imageView = view.findViewById(R.id.image_view);

        imageView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(context, LogActivity.class);

                activity.startActivity(intent);
            }
        });

        return new MyViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {
        Bitmap image = DataManager.getinstance().getImage(DataManager.getinstance().getNotFinishKeyList().get(position));
        //TODO : 비트맵으로 이미지 받아와서 실행
        holder.imageView.setImageBitmap(image);

    }

    @Override
    public int getItemCount() {
        return DataManager.getinstance().getNotFinishKeyList().size();
    }

    public void update()
    {
        DataManager.getinstance().updateNotFinishList();
        notifyDataSetChanged();
    }

    public class MyViewHolder extends RecyclerView.ViewHolder {
        private ImageView imageView;
        private Button yes_button;
        private Button no_button;

        public MyViewHolder(@NonNull View itemView) {
            super(itemView);

            imageView = itemView.findViewById(R.id.image_view);
        }
    }




}
