from enum import Enum

class State(Enum) :
    NOT_FILL = 1
    FILLING = 2
    FINISH = 3

class Code :
    DATA = "DATA_"
    SIZE = "SIZE_"
    STATE = "FILL_"
    CONN = "CONN"