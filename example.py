"""Run this bridge on one MicroPython device; reporting_device.py on another."""
import network
import espnow

station = network.WLAN(network.STA_IF)
station.active(True)
radio = espnow.ESPNow()
radio.active(True)
while True:
    host, message = radio.recv(30000)
    if not host or not message:
        continue
    radio.add_peer(host)
    try:
        response = ('Channel:' + str(station.config('channel'))).encode() if message == b'ESPNOW' else b'Success'
        radio.send(host, response, True)
    finally:
        radio.del_peer(host)
