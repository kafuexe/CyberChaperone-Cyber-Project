from scapy.all import sniff, DNSQR , IP
import time
import socket

stop = False
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
while not stop:
    try:
        pkts = sniff(filter="udp and port 53", count=1)

        for pkt in pkts:
            if (pkt[IP].src == IPAddr):
                pkt.show()

            time_string = time.strftime("%m/%d/%Y, %H-%M-%S", time.localtime())

            msg = f"{time_string}:[PORT 53]:{str(pkt[DNSQR].qname.decode())}"
            print(msg)
            time.sleep(0.5)
    except Exception as e:
        stop = True