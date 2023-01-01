import Server
import threading
from DroneControl import DroneControl

# server = Server.Server()
# DroneControl = server.getDroneObject()

DroneControl = DroneControl()
# droneThread = threading.Thread(target=DroneControl.run())
# droneThread.start()
DroneControl.run()

# server.run()