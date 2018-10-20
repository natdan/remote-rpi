#################################################################################
# Copyright (c) 2018 Creative Sphere Limited.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License v2.0
# which accompanies this distribution, and is available at
# https://www.apache.org/licenses/LICENSE-2.0
#
#  Contributors:
#    Creative Sphere - initial API and implementation
#
#################################################################################

import os
import socket

SPI_COMMAND = 0b00100000
SPI_CLOSE = SPI_COMMAND | 1
SPI_OPEN = SPI_COMMAND | 2
SPI_XFER = SPI_COMMAND | 3

I2C_COMMAND = 0b01000000

SERIAL_COMMAND = 0b01100000

GPIO_COMMAND = 0b10000000

NRF_COMMAND = 0b10100000
NRF_INIT = NRF_COMMAND | 1
NRF_CLOSE = NRF_COMMAND | 2
NRF_SET_READ_PIPE_ADR = NRF_COMMAND | 3
NRF_SET_WRITE_PIPE_ADR = NRF_COMMAND | 4
NRF_GET_READ_PIPE_ADR = NRF_COMMAND | 5
NRF_GET_WRITE_PIPE_ADR = NRF_COMMAND | 6
NRF_FLUSH_TX = NRF_COMMAND | 7
NRF_FLUSH_RX = NRF_COMMAND | 8
NRF_POWER_UP = NRF_COMMAND | 9
NRF_POWER_DOWN = NRF_COMMAND | 10
NRF_SWITCH_TX = NRF_COMMAND | 11
NRF_SWITCH_RX = NRF_COMMAND | 12
NRF_RESET = NRF_COMMAND | 13
NRF_SEND = NRF_COMMAND | 14
NRF_RECEIVE = NRF_COMMAND | 15
NRF_START_LISTENING = NRF_COMMAND | 16
NRF_STOP_LISTENING = NRF_COMMAND | 17
NRF_POOL_DATA = NRF_COMMAND | 18
NRF_SEND_AND_RECEIVE = NRF_COMMAND | 19


class RRPi:
    _socket = None

    def __init__(self):
        port = 8789
        ip = os.environ["RASPBERRY_IP"]
        if "RASPBERRY_PORT" in os.environ:
            port = int(os.environ["RASPBERRY_PORT"])

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((ip, port))

    def close(self):
        self._socket.close()

    def send(self, data):
        self._socket.send(data)

    def sendInt(self, value):
        buf = bytearray()
        buf.append(value)
        self._socket.send(buf)

    def recv(self, len):
        return self._socket.recv(len)

    def recvBool(self):
        return False if ord(self._socket.recv(1)) == 0 else True

    def recvInt(self):
        return ord(self._socket.recv(1))


def intArrayToBuffer(array, buf):
    for b in  array:
        buf.append(b)

    return buf


def bytesToIntArray(bb):
    res = []
    for b in bb:
        res.append(int(b))

    return res
