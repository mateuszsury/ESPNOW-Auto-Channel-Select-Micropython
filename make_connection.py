def make_connection(WLAN_STA, ESPNowObject, peer):
    for channel in range (1, 15):
        first_message = "ESPNOW"
        print("Trying to connect at channel: " + str(channel))
        WLAN_STA.config(channel = channel)
        ESPNowObject.send(peer, first_message, True)
        host, msg = ESPNowObject.recv(3000)
        time.sleep(2)
        if msg:
            mess = str(msg)[2:-1]
            if ':' in mess:
                key, value = mess.split(':')
                if key == 'Channel':
                    WLAN_STA.config(channel = int(value))
                    print("Channel set to: " + value)
                    break
        if channel == 14:
            print("Peer not found, trying again")
            channel = 1
