package util;

public class Network {
    static public final String serverIP = "192.168.0.85";
    static public final String webStreamingURL = "http://192.168.0.85:5000/video_feed";
    static public final int port = 9000;
    static public int packetSize = 4096;

    static public final String IMG_SIZE = "SIZE_";
    static public final String IMG_DATA = "DATA_";
    static public final String IMG_STATE = "FILL_";
    static public final String IMG_WANT = "WANT_";
    static public final String CONNECT = "CONN_";

    static public String CreateSendMessage(String id, String code, String data)
    {
        return id + code + " : " + data;
    }
}
