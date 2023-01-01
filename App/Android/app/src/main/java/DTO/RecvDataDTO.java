package DTO;

import util.Network;

public class RecvDataDTO {
    byte[] action;
    byte[] data;

    public RecvDataDTO(byte[] bytes)
    {
        byte[] actionTemp = new byte[128];
        byte[] dataTemp = new byte[Network.packetSize - 128];
        int offset = 0;


        for(int i = 0 ; i < bytes.length; ++i)
        {
            byte b1 = bytes[i];
            byte b2 = bytes[i + 1];
            byte b3 = bytes[i + 2];

            if(b1 == 32 && b2 == 58 && b3 == 32)
            {
                offset = i;
                break;
            }
            actionTemp[i] = bytes[i];
        }

        System.arraycopy(bytes, offset + 3, dataTemp, 0, dataTemp.length - (offset + 3));

        action = actionTemp;
        data = dataTemp;
    }

    public byte[] getAction() {
        return action;
    }

    public byte[] getData() {
        return data;
    }
}
