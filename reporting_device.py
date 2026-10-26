"""Replace PEER with the bridge MAC before copying to the reporting device."""
import network
import espnow
import time
from make_connection import make_connection

PEER = bytes.fromhex('aabbccddeeff')
station = network.WLAN(network.STA_IF)
station.active(True)
radio = espnow.ESPNow()
radio.active(True)
radio.add_peer(PEER)
while True:
    # Configure the permitted channels for your board and jurisdiction.
    channel = make_connection(station, radio, PEER, channels=range(1, 12))
    if channel is None:
        time.sleep(2)
        continue
    try:
        radio.send(PEER, b'temperature=25', True)
        radio.recv(3000)
    except OSError:
        pass
    time.sleep(2)
