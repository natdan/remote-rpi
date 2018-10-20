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

import rrpi
import struct
import time

_rrpi = None

DEBUG = False

def delay10us():
    time.sleep(0.00001)


def delay20ms():
    time.sleep(0.02)


def delay2ms():
    time.sleep(0.002)


def delay100ms():
    time.sleep(0.1)


def setReadPipeAddress(pipeNumber, address):
    buf = bytearray()
    buf.append(rrpi.NRF_SET_READ_PIPE_ADR)
    buf.append(pipeNumber)

    _rrpi.send(rrpi.intArrayToBuffer(address, buf))

    if DEBUG:
        print(">> sent NRF_SET_READ_PIPE_ADR " + str(pipeNumber) + ", " + str(address))


def setWritePipeAddress(address):
    buf = bytearray()
    buf.append(rrpi.NRF_SET_WRITE_PIPE_ADR)
    _rrpi.send(rrpi.intArrayToBuffer(address, buf))

    if DEBUG:
        print(">> sent NRF_SET_WRITE_PIPE_ADR " + str(address))


def getWritePipeAddress():
    raise NotImplemented()


def writeFlushTX():
    _rrpi.sendInt(rrpi.NRF_FLUSH_TX)

    if DEBUG:
        print(">> sent NRF_FLUSH_TX")


def writeFlushRX():
    _rrpi.sendInt(rrpi.NRF_FLUSH_RX)

    if DEBUG:
        print(">> sent NRF_FLUSH_RX")


def initNRF(spiBus, spiDevice, packetSize, address, channel):
    global _rrpi

    _rrpi = rrpi.RRPi()
    buf = bytearray()
    buf.append(rrpi.NRF_INIT)
    buf.append(spiBus)
    buf.append(spiDevice)
    buf.append(packetSize)
    rrpi.intArrayToBuffer(address, buf)
    buf.append(channel)
    _rrpi.send(buf)

    if DEBUG:
        print(">> sent NRF_INIT")


def powerUp():
    _rrpi.sendInt(rrpi.NRF_POWER_UP)

    if DEBUG:
        print(">> sent NRF_FLUSH_TX")


def powerDown():
    _rrpi.sendInt(rrpi.NRF_POWER_DOWN)

    if DEBUG:
        print(">> sent NRF_POWER_DOWN")


def swithToTX():
    _rrpi.sendInt(rrpi.NRF_SWITCH_TX)

    if DEBUG:
        print(">> sent NRF_SWITCH_TX")


def swithToRX():
    _rrpi.sendInt(rrpi.NRF_SWITCH_RX)

    if DEBUG:
        print(">> sent NRF_SWITCH_RX")


def reset():
    _rrpi.sendInt(rrpi.NRF_RESET)

    if DEBUG:
        print(">> sent NRF_RESET")


def sendString(data):
    sendString(_stringToBytes(data))


def sendData(data):
    buf = bytearray()
    buf.append(rrpi.NRF_SEND)
    buf.append(len(data))
    _rrpi.send(rrpi.intArrayToBuffer(data, buf))

    res = _rrpi.recvBool()

    if DEBUG:
        print(">> sent NRF_SEND, get " + str(res))
    return res


def _stringToBytes(s):
    b = bytearray()
    b.extend(map(ord, s))
    return b


def padToSize(buf, size):
    while len(buf) < size:
        buf.append(0)

    return buf


def startListening():
    _rrpi.sendInt(rrpi.NRF_START_LISTENING)

    if DEBUG:
        print(">> sent NRF_START_LISTENING")


def stopListening():
    _rrpi.sendInt(rrpi.NRF_STOP_LISTENING)

    if DEBUG:
        print(">> sent NRF_STOP_LISTENING")


def receiveData(n):
    buf = bytearray()
    buf.append(rrpi.NRF_RECEIVE)
    buf.append(n)
    _rrpi.send(buf)
    data = rrpi.bytesToIntArray(_rrpi.recv(n))

    if DEBUG:
        print(">> sent NRF_RECEIVE, got " + str(data))
    return data


def poolData(timeout):
    buf = bytearray()
    buf.append(rrpi.NRF_POOL_DATA)
    rrpi.intArrayToBuffer(struct.pack("f", timeout), buf)
    _rrpi.send(buf)
    res = _rrpi.recvBool()

    if DEBUG:
        print(">> sent NRF_POOL_DATA, got " + str(res))
    return res


def sendAndReceive(data, timeout):
    buf = bytearray()
    buf.append(rrpi.NRF_SEND_AND_RECEIVE)
    rrpi.intArrayToBuffer(struct.pack("f", timeout), buf)
    size = len(data)
    buf.append(size)
    _rrpi.send(rrpi.intArrayToBuffer(data, buf))
    time.sleep(0.001)
    recieved = _rrpi.recv(size)
    res = rrpi.bytesToIntArray(recieved)

    if DEBUG:
        print(">> sent NRF_SEND_AND_RECEIVE; set= " + str(data) + ", " + str(timeout) + ", got= " + str(res))
    return res


def close():
    _rrpi.sendInt(rrpi.NRF_CLOSE)

    if DEBUG:
        print(">> sent NRF_CLOSE")
