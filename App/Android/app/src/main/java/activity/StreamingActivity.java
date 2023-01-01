package activity;

import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.os.Bundle;
import android.view.View;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.widget.ImageView;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import com.root.myapplication.R;

import util.Network;

public class StreamingActivity extends AppCompatActivity {

    ImageView fullScreen;
    WebView webView;
    WebSettings webSettings;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.streaming_activity);

        fullScreen = findViewById(R.id.iv_full_screen);
        webView = findViewById(R.id.web_view_streaming);

        webSettings = webView.getSettings();
        webSettings.setJavaScriptEnabled(true);
        webView.setVerticalScrollBarEnabled(false);
        webView.setHorizontalScrollBarEnabled(false);
        webView.setInitialScale(100);

        webView.loadDataWithBaseURL(null,creHtmlBody(Network.webStreamingURL), "text/html", "utf-8", null);

        fullScreen.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(StreamingActivity.this, FullScreenActivity.class);

                startActivity(intent);
            }
        });

    }

    public String creHtmlBody(String imagUrl)
    {
        StringBuffer sb = new StringBuffer("<HTML>");
        sb.append("<HEAD>");
        sb.append("</HEAD>");
        sb.append("<BODY style='margin:0; padding:0; text-align:center;'>");//중앙정렬
        sb.append("<img width='100%' height='100%' src=\"" + imagUrl+"\">"); //가득차게 나옴
        sb.append("</BODY>");
        sb.append("</HTML>");

        return sb.toString();
    }


}
