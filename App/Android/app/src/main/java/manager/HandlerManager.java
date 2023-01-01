package manager;

import android.os.Handler;
import android.os.Message;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.Queue;

import DTO.HandlerInfo;
import thread.HandlerManagerThread;

public class HandlerManager {
    private static HandlerManager instance = null;
    private HashMap<String, Handler> dataMap;
    private Queue<HandlerInfo> handlerQueue;
    private boolean isRun = false;
    private HandlerManagerThread thread;

    private HandlerManager()
    {
        dataMap = new HashMap<>();
        handlerQueue = new LinkedList<>();
        thread = new HandlerManagerThread();
        thread.start();

    }

    public static HandlerManager getInstance() {

        if (instance == null)
            instance = new HandlerManager();

        return instance;
    }

    public void finalize()
    {
        thread.stopThread();
    }

    public void putHandler(String key, Handler handler)
    {
        if(!dataMap.containsKey(key))
            dataMap.put(key, handler);
    }

    public Handler getHandler(String key)
    {
        if(dataMap.containsKey(key))
            return dataMap.get(key);

        return null;
    }

    public boolean isRun()
    {
        return isRun;
    }

    public void setRun(boolean run)
    {
        isRun = run;
    }

    public HandlerInfo poll()
    {
        return handlerQueue.poll();
    }

    public void offer(String key, Message message)
    {
        handlerQueue.offer(new HandlerInfo(dataMap.get(key), message));
    }

    public int size()
    {
        return handlerQueue.size();
    }
}
