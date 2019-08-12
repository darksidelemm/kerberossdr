#!/usr/bin/env python
#
# 	Kerberos SDR - Chasemapper Connection
#
#   Copyright (C) 2018  Mark Jessop <vk5qi@rfhead.net>
#   Released under GNU GPL v3 or later
#
import socket


def emit_bearing_msg(bearing=0.0, confidence=100.0, udp_port=55673):
    packet = {
        'type' : 'BEARING',
        'bearing' : bearing,
        'confidence': confidence,
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
        s.sendto(json.dumps(packet), ('<broadcast>', udp_port))
    except socket.error:
        s.sendto(json.dumps(packet), ('127.0.0.1', udp_port))