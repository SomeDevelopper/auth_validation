from datetime import datetime, date, timedelta

# BCI

'''
Delta δ (0.5-4 Hz): Deeply asleep/not dreaming

Theta θ (4-8 Hz): Sleep, deep relaxation, and visualization

Alpha α (8-13 Hz): Relaxed and calm

Beta β (13-32 Hz): Actively thinking or problem-solving

Gamma γ (32-100 Hz): Hyper brain activity, great for learning
'''

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
# dispatcher.map("/muse/eeg", eeg_handler, "EEG")
dispatcher.map("/muse/gyro", gyr_handler, "GYR")
server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
print("Listening on UDP port "+str(port))
server.serve_forever()