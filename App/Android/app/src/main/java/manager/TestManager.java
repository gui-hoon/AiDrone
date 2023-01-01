package manager;

import android.media.Image;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class TestManager {
    private static TestManager instance = null;
    private HashMap<String, String> dataMap;


    public static TestManager Get()
    {
        if(instance == null)
            instance = new TestManager();
        return instance;
    }

    private TestManager()
    {
        dataMap = new HashMap<>();
    }

    public void addImage(String key, String test)
    {
        if(dataMap.containsKey(key))
            return;

        dataMap.put(key, test);
    }

    public List<String> getKeys()
    {
        List<String> output = new ArrayList<>();
        for(String key : dataMap.keySet())
        {
            output.add(key);
        }

        return output;
    }

    public String getImage(String key)
    {
        if(dataMap.containsKey(key))
            return dataMap.get(key);

        return null;
    }

    public int getSize()
    {
        return dataMap.size();
    }

}
