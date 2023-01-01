class ClientStatus :
    port : int
    isRunThread : bool
    isLatestVersion : bool

    def __init__(self, port, isRunThread, isLatestVersion) :
        self.isLatestVersion = isLatestVersion
        self.port = port
        self.isRunThread = isRunThread

