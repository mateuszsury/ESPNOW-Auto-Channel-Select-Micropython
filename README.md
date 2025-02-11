# ESPNOW-Auto-Channel-Select-Micropython

A MicroPython library that automates the process of selecting the correct Wi-Fi channel for ESPNOW communications. This project provides a utility function to scan channels and establish a connection with a peer device by dynamically setting the channel. It also includes example implementations for both a WiFi Bridge and an ESPNOW Reporting Device.

---

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Library Function: `make_connection`](#library-function-make_connection)
  - [Example: WiFi Bridge](#example-wifi-bridge)
  - [Example: ESPNOW Reporting Device](#example-espnow-reporting-device)
- [Dependencies](#dependencies)
- [License](#license)

---

## Introduction

ESP-NOW is a connectionless communication protocol developed by Espressif that allows multiple devices to exchange data without a traditional Wi-Fi network. However, when multiple channels are in use, establishing a reliable connection can be challenging. This library automates the channel selection process by scanning through available channels (1–14) until it locates a responsive peer device. Once found, it adjusts the device's channel to match the peer for optimal communication.

---

## Features

- **Automatic Channel Selection:**  
  Scans through channels 1 to 14 to find and establish a connection with the target peer.
  
- **Dynamic Channel Adjustment:**  
  Once the peer responds with its current channel, the local device updates its configuration accordingly.
  
- **Easy Integration:**  
  Minimal code required to integrate this functionality into your existing ESPNOW projects.
  
- **Example Implementations:**  
  Includes sample code for a WiFi Bridge and an ESPNOW Reporting Device to help you get started.

---

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/mateuszsury/ESPNOW-Auto-Channel-Select-Micropython.git
   ```
2. **Copy Files to Your Device:**
   Use your preferred tool (e.g., ampy, rshell, or your IDE's file manager) to transfer the files to your MicroPython-enabled device.

3. **Ensure Required Modules:**
   Make sure your device's MicroPython firmware supports the following modules:
   - `network`
   - `espnow`
   - `time`
   - `random`

---

## Usage

### Library Function: `make_connection`

The core function of this project is `make_connection`, which iterates over channels 1 through 14, sending a connection request until a peer device responds with its current channel setting. Once the response is received, the function updates the device's Wi-Fi channel accordingly.

#### Function Definition
```python
def make_connection(WLAN_STA, ESPNowObject, peer):
    for channel in range(1, 15):
        first_message = "ESPNOW"
        print("Trying to connect at channel: " + str(channel))
        WLAN_STA.config(channel=channel)
        ESPNowObject.send(peer, first_message, True)
        host, msg = ESPNowObject.recv(3000)
        time.sleep(2)
        if msg:
            mess = str(msg)[2:-1]
            if ':' in mess:
                key, value = mess.split(':')
                if key == 'Channel':
                    WLAN_STA.config(channel=int(value))
                    print("Channel set to: " + value)
                    break
        if channel == 14:
            print("Peer not found, trying again")
            channel = 1 
```

### Example: WiFi Bridge

The following example demonstrates a WiFi Bridge that listens for ESPNOW messages and responds with its current channel information when it receives a connection request.

```python
import network
import espnow

sta = network.WLAN(network.STA_IF)
sta.active(True)

e = espnow.ESPNow()
e.active(True)

while True:
    host, msg = e.recv(30000)
    if msg:
        print(msg)
        channel_mess = str(msg)[2:-1]
        if channel_mess == "ESPNOW":
            e.add_peer(host)
            server_channel = "Channel:" + str(sta.config('channel'))
            e.send(host, server_channel, True)
            e.del_peer(host)
        else:
            e.add_peer(host)
            success = "Success"
            e.send(host, success, True)
            e.del_peer(host)
```

### Example: ESPNOW Reporting Device

This example shows how a reporting device can use the `make_connection` function to establish a channel and then periodically send data (e.g., temperature readings) to a peer.

```python
import network
import espnow
import time
import random
from make_connection import make_connection

sta = network.WLAN(network.STA_IF)
sta.active(True)

e = espnow.ESPNow()
e.active(True)

peer = b'@\xaa\xbb\xcc\xdd'
e.add_peer(peer)

while True:
    make_connection(sta, e, peer)
    lost_packets_count = 1
    while True:
        random_number = random.randint(1, 100)
        message = "temperature=" + str(random_number)
        print("Sending message:", message)
        e.send(peer, message, True)
        host_connect, msg_connect = e.recv()
        time.sleep(2)
        if not msg_connect:
            lost_packets_count += 1
            if lost_packets_count > 10:
                print("Connection lost")
                break
```

---

## Dependencies

- **MicroPython Firmware:** Must support the `network`, `espnow`, `time`, and `random` modules.
- **ESPNow Module:** Available as part of the MicroPython firmware on supported ESP devices (e.g., ESP32).
- **Standard Libraries:** `time` and `random` are used for timing functions and generating random numbers.

---

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

---
