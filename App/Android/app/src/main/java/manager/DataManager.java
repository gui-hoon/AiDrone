package manager;

import android.graphics.Bitmap;
import android.media.Image;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

import DTO.ImageDTO;
import adapters.MyAdapter;
import util.State;

public class DataManager {
    private static DataManager dataManager = null;
    private HashMap<String, ImageDTO> dataMap;
    private List<String> keyList;
    private List<String> notFinishKeyList;

    public static DataManager getinstance()
    {
        if(dataManager == null)
            dataManager = new DataManager();
        return dataManager;
    }

    private DataManager()
    {
        dataMap = new HashMap<>();
        keyList = new ArrayList<>();
        notFinishKeyList = new ArrayList<>();
    }

    private void addDTO(String key, ImageDTO dto)
    {
        if(dataMap.containsKey(key))
            return;

        dataMap.put(key, dto);
        keyList.add(key);
    }

    public void setSize(String key, int size)
    {
        if(!dataMap.containsKey(key))
        {
            addDTO(key, new ImageDTO(size, key));
            return;
        }

        dataMap.get(key).setSize(size);
    }

    public void setState(String key, State.Type state)
    {
        if(!dataMap.containsKey(key))
        {
            addDTO(key, new ImageDTO(0, key));
            return;
        }

        dataMap.get(key).setState(state);
    }
    public List<String> getErrorImage()
    {
        List<String> output = new ArrayList<>();

        for(String key : keyList)
        {
            if(dataMap.get(key).isError())
            {
                output.add(key);
            }
        }

        return output;
    }

    public ImageDTO getImageDTO(String key)
    {
        if(dataMap.containsKey(key))
            return dataMap.get(key);

        return null;
    }

    public List<String> getKeys()
    {
        return keyList;
    }

    public Bitmap getImage(String key)
    {
        if(dataMap.containsKey(key))
            return dataMap.get(key).getImage();

        return null;
    }

    public State.Type getState(String key)
    {
        if(dataMap.containsKey(key))
            return dataMap.get(key).getState();

        return null;
    }

    public int getSize()
    {
        return dataMap.size();
    }

    public boolean containsKey(String key)
    {
        return dataMap.containsKey(key);
    }

    public void pushImageData(String key, byte[] data)
    {
        if(containsKey(key))
            dataMap.get(key).addImageData(data);
    }

    public String getKeyFromPosition(int pos)
    {
        if(keyList.size() < pos)
            return null;

        return keyList.get(pos);
    }

    public String getKeyNotFinishDataFromPosition(int pos)
    {
        if(pos < 0)
            pos = 0;

        if(notFinishKeyList.size() == 0)
            return "";

        if(pos >= notFinishKeyList.size())
            return getLastImageName();

        return notFinishKeyList.get(pos);
    }

    public int getSizeNotFinishList()
    {
        return getNotFinishKeyList().size();
    }

    public List<String> getNotFinishKeyList()
    {
        return new ArrayList<>(notFinishKeyList);
    }

    public int getPosFromImageName(String ImageName)
    {
        for(int i = 0; i < notFinishKeyList.size(); ++i)
        {
            String key = notFinishKeyList.get(i);

            if(key == ImageName)
                return i;
        }

        return -1;
    }

    public String getLastImageName()
    {
        if(notFinishKeyList.size() == 0)
            return "";
        else
            return notFinishKeyList.get(notFinishKeyList.size() - 1);
    }

    public void updateNotFinishList()
    {
        notFinishKeyList.clear();

        for(String key : keyList)
        {
            if(getState(key) != State.Type.FINISHED)
                notFinishKeyList.add(key);
        }
    }
}
