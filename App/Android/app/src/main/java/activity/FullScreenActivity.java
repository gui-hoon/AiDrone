package activity;

import android.app.Activity;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.os.Bundle;
import android.view.View;
import android.view.Window;
import android.webkit.WebSettings;
import android.webkit.WebView;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import com.root.myapplication.R;

import util.Network;


public class FullScreenActivity extends AppCompatActivity {
    WebView webView;
    WebSettings webSettings;

    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        requestWindowFeature(Window.FEATURE_NO_TITLE);
        setContentView(R.layout.streaming_full_screen);
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE);

        webView = findViewById(R.id.wv_full_screen);
        webSettings = webView.getSettings();
        webSettings.setJavaScriptEnabled(true);
        webView.setVerticalScrollBarEnabled(false);
        webView.setHorizontalScrollBarEnabled(false);
        webView.setInitialScale(100);

        webView.loadDataWithBaseURL(null,creHtmlBody(Network.webStreamingURL), "text/html", "utf-8", null);

    }


    private String creHtmlBody(String imagUrl)
    {
        StringBuffer sb = new StringBuffer("<HTML>");
        sb.append("<HEAD>");
        sb.append("</HEAD>");
        sb.append("<BODY style='margin:0; padding:0; text-align:center;'>");//중앙정렬
        sb.append("<img width='100%' height='100%' src=\"" + imagUrl + "\">"); //가득차게 나옴
        sb.append("</BODY>");
        sb.append("</HTML>");

        return sb.toString();
    }

    @Override
    public void onBackPressed() {
        super.onBackPressed();
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
        Intent intent = new Intent(FullScreenActivity.this, StreamingActivity.class); //지금 액티비티에서 다른 액티비티로 이동하는 인텐트 설정
        intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);    //인텐트 플래그 설정
        startActivity(intent);  //인텐트 이동
        finish();   //현재 액티비티 종료
    }
}
