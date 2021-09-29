
import time
import sys
from socket import *
from datetime import datetime

serverIP = sys.argv[1]
serverPort = int(sys.argv[2])

# UDP socket
UserSocket = socket(AF_INET, SOCK_DGRAM)
addr = (serverIP, serverPort)

L_rtts = []
P_loss =0

for i in range(15):
    # current time
    time_stamp = datetime.now().isoformat(sep = ' ')[:-3]

    info_ping = f'{i+100} PING' + str(i) + ' ' + time_stamp + '\r\n'
    T_send = datetime.now()
    # send message
    UserSocket.sendto(info_ping.encode(), addr)

    try:
        UserSocket.settimeout(0.4)
        message, address = UserSocket.recvfrom(1024)
        T_receive = datetime.now()

        rtt = round((T_receive - T_send).total_seconds() * 1000)
        L_rtts.append(rtt)

        print(f'{100+i} PING to {serverIP}, seq={i}, rtt={rtt} ms')
        UserSocket.settimeout(None)

    except timeout:
        P_loss = P_loss + 1
        print(f'{100+i} PING to {serverIP}, seq={i}, rtt= time out')

print("\n")
print(f'Minimum RTT = {min(L_rtts)} ms')
print(f'Maximum RTT = {max(L_rtts)} ms')
sum, len = sum(L_rtts), len(L_rtts)
print(f'Average RTT = {round(float(sum/len))} ms')
print(f'{float(P_loss)/10 * 100}% of packets have been lost through the network')

