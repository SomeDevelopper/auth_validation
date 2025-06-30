from datetime import datetime, date, timedelta

# BCI

def eeg_handler(address: str, *args):
    dateTimeObj = datetime.now()
    printStr = dateTimeObj.strftime("%Y-%m-%d %H:%M:%S.%f")
    for arg in args:
        printStr += ","+str(arg)
    print(printStr)


def gyr_handler(address: str, *args):
    dateTimeObj = datetime.now()
    printStr = dateTimeObj.strftime("%Y-%m-%d %H:%M:%S.%f")
    for arg in args:
        printStr += ","+str(arg)

    print(printStr)
    if (int(args[3]) > 0 and int(args[3]) >= 100):
        print('RIGHT')

    if (int(args[3]) < 0 and int(args[3]) <= -100):
        print('LEFT')

ip = "0.0.0.0"
port = 5005
from pythonosc import dispatcher
from pythonosc import osc_server
dispatcher = dispatcher.Dispatcher()
dispatcher.map("/muse/eeg", eeg_handler, "EEG")
# dispatcher.map("/muse/gyro", gyr_handler, "GYR")
server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
print("Listening on UDP port "+str(port))
server.serve_forever()