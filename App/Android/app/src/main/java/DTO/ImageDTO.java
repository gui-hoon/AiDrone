package DTO;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Message;
import android.util.Log;

import manager.DataManager;
import manager.HandlerManager;
import util.Network;
import util.State;

public class ImageDTO {
    private int size;
    private int count;
    private byte[] buffer;
    private int offset;
    private String imageName;
    private State.Type state;
    private Bitmap image;

    public State.Type getState() {
        return state;
    }

    public void setState(State.Type state) {
        this.state = state;
    }

    public ImageDTO(int size, String imageName)
    {
        this.size = size;
        this.imageName = imageName;
        state = State.Type.NOT_FILL;
        image = null;
        count = 0;
        offset = 0;
        buffer = new byte[Network.packetSize * size];
    }

    public Bitmap getImage() {
        return image;
    }

    private void createImage()
    {
        image = BitmapFactory.decodeByteArray(buffer, 0, offset);
        HandlerManager.getInstance().offer("AdapterHandler", new Message());
        HandlerManager.getInstance().offer("CountHandler", new Message());
    }


    public void setImage(Bitmap image) {
        this.image = image;
    }

    public int getSize() {
        return size;
    }

    public void setSize(int size) {
        this.size = size;
        buffer = new byte[Network.packetSize * size];
    }

    public void addImageData(byte[] data)
    {
        try{
            System.arraycopy(data, 0, buffer, offset, data.length);
        }
        catch(ArrayIndexOutOfBoundsException e)
        {
            e.printStackTrace();
        }
        offset += data.length;
        count++;

        if(count == size)
            createImage();
    }

    public boolean isError()
    {
        return count != size;
    }

    public void bufferClear()
    {
        buffer = new byte[Network.packetSize * size];
        image = null;
        count = 0;
        offset = 0;
    }




}
