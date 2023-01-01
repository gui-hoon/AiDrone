package thread;

import android.os.Handler;
import android.os.Message;


import DTO.HandlerInfo;
import manager.HandlerManager;

public class HandlerManagerThread extends Thread{

    private boolean run = true;

    @Override
    public void run() {
        super.run();

        while(run)
        {
            if(!HandlerManager.getInstance().isRun())
            {
                if(HandlerManager.getInstance().size() <= 0)
                    continue;

                HandlerInfo handlerInfo = HandlerManager.getInstance().poll();

                if(handlerInfo == null)
                    continue;

                HandlerManager.getInstance().setRun(true);

                Handler handler = handlerInfo.getHandler();
                Message message = handlerInfo.getMessage();

                handler.sendMessage(message);


            }
        }
    }

    public void stopThread()
    {
        run = false;
    }
}
