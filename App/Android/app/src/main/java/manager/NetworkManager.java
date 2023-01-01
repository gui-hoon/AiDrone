package manager;

//통신은 UDP로하고 이미지는 bitmap으로 처리

//상태변환
//FILL_[ImageName] : 1 or 2 or 3
//0. 안채움
//1. 채우는중
//2. 다채움
//
//이미지 사이즈 전송
//SIZE_[ImageName] : 사이즈
//
//이미지 데이터 받기
//RECV_[ImageName] : 데이터
//
//서버 연결
//CONN

import android.content.Context;
import android.graphics.Color;
import android.graphics.drawable.ColorDrawable;
import android.util.Log;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketTimeoutException;
import java.nio.charset.StandardCharsets;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;

import DTO.RecvDataDTO;
import dialog.ProgressDialog;
import util.Network;
import util.State;
import util.Util;

public class NetworkManager {

    private boolean isConnct;
    private InetAddress serverAddr;
    private DatagramSocket socket;
    private Queue<RecvQueueInfo> recvQueue;
    private String id;

    private static NetworkManager instance = null;

    public static void Create()
    {
        if(instance == null)
            instance = new NetworkManager();
    }

    public static NetworkManager getInstance() {

        if (instance == null)
            return null;

        return instance;
    }
    private NetworkManager() {
        try {
            isConnct = false;
            socket = new DatagramSocket();
            serverAddr = InetAddress.getByName(Network.serverIP);
            recvQueue = new LinkedList<>();
            id = "00000000";
        }
        catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void tryConnect(Context context)
    {
        ProgressDialog dialog = new ProgressDialog(context);
        dialog.getWindow().setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));
        dialog.setCancelable(false);
        dialog.show();


        Thread connectThread = new Thread(() -> {
            while (true) {

                send(Network.CreateSendMessage(id, Network.CONNECT, ""));
                int count = 0;
                byte[] bytes = new byte[Network.packetSize];
                DatagramPacket recvPacket = new DatagramPacket(bytes, bytes.length);

                try {
                    socket.setSoTimeout(1000);
                    socket.receive(recvPacket);
                } catch (SocketTimeoutException e) {

                    if(count >= 3)
                        break;

                    count++;

                } catch (IOException e) {
                    e.printStackTrace();
                }

                String recvStr = new String(recvPacket.getData()).trim();

                if (recvStr.contains(Network.CONNECT))
                {
                    recvStr = recvStr.replace(Network.CONNECT, "");
                    id = recvStr;
                    isConnct = true;
                    runRecvThread();
                    queueThread();
                    break;
                }
            }

        });

        connectThread.start();

        new Thread(() -> {
            while (true) {
                if(!connectThread.isAlive())
                {
                    HandlerManager.getInstance().offer("ConnectHandler", Util.getMessage("value", isConnected()));
                    dialog.dismiss();
                    break;
                }
            }
        }).start();

    }

    public boolean isConnected()
    {
        return isConnct;
    }


    public void runRecvThread()
    {
        //recv
        new Thread(() -> {
            while(true)
            {
                try {
                    byte[] bytes = new byte[Network.packetSize];
                    DatagramPacket recvPacket = new DatagramPacket(bytes, bytes.length);

                    socket.setSoTimeout(3000);
                    socket.receive(recvPacket);
                    recvQueue.offer(new RecvQueueInfo() {
                        @Override
                        public void run() {
                            RecvDataDTO dto = new RecvDataDTO(recvPacket.getData());
                            String recvAction = new String(dto.getAction()).trim();

                            if(recvAction.contains(Network.IMG_STATE))
                            {
                                String imageName = recvAction.replace(Network.IMG_STATE, "");
                                String strData = new String(dto.getData()).trim();
                                DataManager.getinstance().setState(imageName, State.getType(strData));

                                HandlerManager.getInstance().offer("StateHandler", Util.getMessage("state", State.getTypeToInt(DataManager.getinstance().getState(imageName))));
                            }

                            else if(recvAction.contains(Network.IMG_SIZE))
                            {
                                String imageName = recvAction.replace(Network.IMG_SIZE, "");
                                String strData = new String(dto.getData()).trim();
                                int size = Integer.parseInt(strData);
                                Log.d("ImageName", imageName);
                                DataManager.getinstance().setSize(imageName, size);
                            }

                            else if(recvAction.contains(Network.IMG_DATA)) {
                                String imageName = recvAction.replace(Network.IMG_DATA, "");

                                DataManager.getinstance().pushImageData(imageName, dto.getData());
                            }
                        }
                    });

                } catch (SocketTimeoutException e) {
                    Log.d("타임아웃 어쩌구", "");

                    if(!recvQueue.isEmpty())
                        continue;

                    List<String> errorImages = DataManager.getinstance().getErrorImage();
                    if(errorImages.isEmpty())
                    {
                        send(Network.CreateSendMessage(id, Network.IMG_WANT,  DataManager.getinstance().getSize() + ""));
                    }
                    else
                    {
                        String key = errorImages.get(0);
                        DataManager.getinstance().getImageDTO(key).bufferClear();
                        send(Network.CreateSendMessage(id, Network.IMG_WANT,  key));
                    }
                    e.printStackTrace();
                } catch (IOException e) {
                    Log.d("IO 어쩌구", "");
                    e.printStackTrace();
                }
            }
        }).start();
    }

    public void queueThread()
    {
        new Thread(() ->
        {
           while(true)
           {
               if(recvQueue.size() <= 0)
                   continue;

               RecvQueueInfo info = recvQueue.poll();
               if(info == null)
                   continue;

               info.run();
           }
        }).start();
    }

    public void send(byte[] bytes)
    {
        new Thread(() -> {
            try {
                DatagramPacket sendData = new DatagramPacket(bytes, bytes.length, serverAddr, Network.port);
                socket.send(sendData);
            }
            catch (IOException e) {
                e.printStackTrace();
            }
        }).start();
    }

    public void send(String str)
    {
        byte[] bytes = str.getBytes(StandardCharsets.UTF_8);
        send(bytes);
    }

    private abstract class RecvQueueInfo
    {
        public abstract void run();
    }

    public String getId() {
        return id;
    }
}
