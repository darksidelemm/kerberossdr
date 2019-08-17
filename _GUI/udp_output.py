#!/usr/bin/env python
#
# 	Kerberos SDR - Chasemapper Connection
#
#   Copyright (C) 2018  Mark Jessop <vk5qi@rfhead.net>
#   Released under GNU GPL v3 or later
#
import json
import socket
import numpy as np


def emit_bearing_msg(bearing=0.0, confidence=100.0, power = -1, raw_bearings = [], raw_doa = [], udp_port=55673):
    packet = {
        'type' : 'BEARING',
        'bearing' : bearing,
        'confidence': confidence,
        'power': power,
        'raw_bearing_angles': list(np.around(raw_bearings,1)),
        'raw_doa': list(np.around(raw_doa,3)),
        'bearing_type': 'relative',
        'source': 'kerberos-sdr'
    }

    # Set up our UDP socket
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.settimeout(1)
    # Set up socket for broadcast, and allow re-use of the address
    s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    except:
        pass
    s.bind(('',udp_port))
    try:
        s.sendto(json.dumps(packet).encode('ascii'), ('<broadcast>', udp_port))
    except socket.error:
        s.sendto(json.dumps(packet).encode('ascii'), ('127.0.0.1', udp_port))