package DTO;

import android.os.Handler;
import android.os.Message;

public class HandlerInfo {
    Handler handler;
    Message message;

    public HandlerInfo(Handler handler, Message message)
    {
        this.handler = handler;
        this.message = message;
    }

    public Handler getHandler() {
        return handler;
    }

    public Message getMessage() {
        return message;
    }
}
