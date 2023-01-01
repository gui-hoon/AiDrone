package util;

public class State {

    public enum Type
    {
        NOT_FILL,
        FILLING,
        FILLING_MINE,
        FINISHED,
        NONE,
    }

    static public Type getType(String type)
    {
        return getType(Integer.parseInt(type));
    }

    static public Type getType(int type)
    {
        int numType = type;

        if(numType == 0)
            return Type.NOT_FILL;
        else if(numType == 1)
            return Type.FILLING;
        else if(numType == 2)
            return Type.FINISHED;
        else if(numType == 3)
            return Type.FILLING_MINE;
        else if(numType == 4)
            return Type.NONE;

        return null;
    }

    static public int getTypeToInt(Type type)
    {
        if(type == Type.NOT_FILL)
            return 0;
        else if(type == Type.FILLING)
            return 1;
        else if(type == Type.FINISHED)
            return 2;
        else if(type == Type.FILLING_MINE)
            return 3;
        else if(type == Type.NONE)
            return 4;

        return -1;
    }
}
