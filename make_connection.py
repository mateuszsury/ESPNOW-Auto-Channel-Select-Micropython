"""A bounded ESP-NOW peer channel discovery pass."""
def make_connection(WLAN_STA, ESPNowObject, peer, channels=range(1, 15), timeout_ms=3000):
    """Return the peer's channel, or None when one complete scan finds no peer.

    Pass only channels permitted by the board and local radio regulations.
    The caller owns retries and has already registered the six-byte peer MAC.
    """
    if len(peer) != 6:
        raise ValueError('peer must be a six-byte MAC address')
    for channel in channels:
        try:
            WLAN_STA.config(channel=channel)
            ESPNowObject.send(peer, b'ESPNOW', True)
            host, message = ESPNowObject.recv(timeout_ms)
        except OSError:
            continue
        if host != peer or not message:
            continue
        try:
            key, value = message.decode('ascii').split(':', 1)
            selected = int(value)
        except (ValueError, UnicodeError, AttributeError):
            continue
        if key == 'Channel' and selected == channel:
            return selected
    return None
