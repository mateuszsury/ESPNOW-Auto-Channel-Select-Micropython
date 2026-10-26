import unittest
from make_connection import make_connection

PEER = b'123456'

class Station:
    def __init__(self): self.channels = []
    def config(self, **kwargs): self.channels.append(kwargs['channel'])

class Radio:
    def __init__(self, replies): self.replies = iter(replies)
    def send(self, *args): pass
    def recv(self, timeout): return next(self.replies)

class DiscoveryTests(unittest.TestCase):
    def test_matches_peer_and_channel(self):
        sta = Station()
        channel = make_connection(sta, Radio([(PEER, b'Channel:2')]), PEER, channels=[2])
        self.assertEqual(channel, 2)
        self.assertEqual(sta.channels, [2])

    def test_ignores_unrelated_and_malformed_replies(self):
        radio = Radio([(b'other!', b'Channel:1'), (PEER, b'Channel:bad'), (PEER, b'Channel:3')])
        self.assertEqual(make_connection(Station(), radio, PEER, channels=[1,2,3]), 3)

    def test_scan_exhaustion_is_bounded(self):
        self.assertIsNone(make_connection(Station(), Radio([(None,None)]), PEER, channels=[1]))

    def test_wrong_mac_length_rejected(self):
        with self.assertRaises(ValueError): make_connection(Station(), Radio([]), b'12345')

if __name__ == '__main__': unittest.main()
