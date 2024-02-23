#WiFi Bridge:

import network
import espnow

sta = network.WLAN(network.STA_IF)
sta.active(True)

e = espnow.ESPNow()
e.active(True)

while True:
    host, msg = self.ESPNowObject.recv(30000)  

    if msg:
        print(msg)
        mess = str(msg)[2:-1].split()
        channel_mess = str(msg)[2:-1]

        if channel_mess == ("ESPNOW"):
            e.add_peer(host)
            server_channel = "Channel:" + str(sta.config('channel'))
            e.send(host, server_channel, True)
            e.del_peer(host)
        else:
            e.add_peer(host)
            success = "Success"
            e.send(host, success, True)
            e.del_peer(host)

#ESPNow reporting device:

import network
import espnow
import time
import random
import make_connection

sta = network.WLAN(network.STA_IF)
sta.active(True)

e = espnow.ESPNow()
e.active(True)

peer = b'@\aa\bb\cc\dd'
e.add_peer(peer)

while True:
    make_connection.make_connection(sta, e, peer)
    lost_packets_count = 1
    while True:
        random_number = random.randint(1, 100)
        message = "temperature=" + str(random_number)
        print("Sending message:", message)  
        e.send(peer, message, True)
        host_connect, msg_connect = e.recv()
        time.sleep(2)
        if not msg_connect:
            i += 1
            if i > 10:
                print("Connection lost")
            break
