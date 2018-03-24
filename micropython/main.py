# main.py -- put your code here!
from network import Sigfox
import socket
import time
from machine import RTC

rtc = RTC()
rtc.init((2014, 5, 1, 4, 13, 0, 0, 0))

# init Sigfox for RCZ1 (Europe)
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)
# create a Sigfox socket
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)
# make the socket blocking
s.setblocking(True)
# configure it as uplink only
s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)

# send some bytes
while True:
    #message = """{{"t":{}}}""".format(str(rtc.now()[-2]))
    message = str(rtc.now()[-2])
    s.send(message)
    print("sent " + message)
    time.sleep(30)
