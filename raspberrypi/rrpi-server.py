#!/usr/bin/env python3

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

import nRF2401
import socket
import spidev
import struct
import threading
import traceback

VERBOSE = 2

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


socketAddress = "0.0.0.0"
port = 8789

if VERBOSE > 2:
    print("Setting up scoket at " + socketAddress + ":" + str(port))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 8789))
s.listen(1)

if VERBOSE > 1:
    print("Listening at " + socketAddress + ":" + str(port))


def intArrayToBuffer(array):
    buf = bytearray()
    for b in array:
        buf.append(b)

    return buf


def bytesToIntArray(byteBuffer):
    res = []
    for b in byteBuffer:
        res.append(int(b))

    return res


def startListen():

    def session(con):

        def returnBoolean(boolValue):
            buf = bytearray()
            buf.append(1 if boolValue else 0)
            con.send(buf)


        def processCommand(cmd):
            if cmd == SPI_CLOSE:
                if VERBOSE > 2:
                    print("SPI: Close")
                try:
                    spi.close()
                except Exception as e:
                    print(str(e))

            elif cmd == SPI_OPEN:
                if VERBOSE > 3:
                    print("SPI: OPEN...")
                bus = ord(con.recv(1))
                device = ord(con.recv(1))
                if VERBOSE > 2:
                    print("SPI: OPEN(" + str(bus) + "." + str(device))
                try:
                    spi.open(bus, device)
                except Exception as e:
                    print(str(e))

            elif cmd == SPI_XFER:
                if VERBOSE > 3:
                    print("SPI: XFER...")
                low = ord(con.recv(1))
                high = ord(con.recv(1))
                size = low + high << 8

                if VERBOSE > 3:
                    print("SPI: XFER(" + str(size) + "), waiting for data...")
                data = con.recv(size)

                if VERBOSE > 2:
                    print("SPI: XFER(" + str(size) + ")")
                try:
                    res = spi.xfer(data)
                    con.send(res)
                except Exception as e:
                    print(str(e))

            elif cmd == NRF_INIT:
                if VERBOSE > 3:
                    print("NRF: INIT...")
                spiBus = ord(con.recv(1))
                spiDevice = ord(con.recv(1))
                packetSize = ord(con.recv(1))
                address = bytesToIntArray(con.recv(5))
                channel = ord(con.recv(1))

                if VERBOSE > 2:
                    print("NRF: INIT(" + str(spiBus) + "." + str(spiDevice) + ", " + str(packetSize) + ", " + str(address) + ", " + str(channel) + ")")
                nRF2401.initNRF(spiBus, spiDevice, packetSize, address, channel)

            elif cmd == NRF_CLOSE:
                if VERBOSE > 3:
                    print("NRF: CLOSE...")
                nRF2401.close()

            elif cmd == NRF_SET_READ_PIPE_ADR:
                if VERBOSE > 3:
                    print("NRF: SET_READ_PIPE_ADDR...")
                pipeNumber = ord(con.recv(1))
                addr = bytesToIntArray(con.recv(5))
                if VERBOSE > 2:
                    print("NRF: SET_READ_PIPE_ADDR(" + str(pipeNumber) + ", " + str(addr) + ")")
                nRF2401.setReadPipeAddress(pipeNumber, addr)

            elif cmd == NRF_SET_WRITE_PIPE_ADR:
                if VERBOSE > 3:
                    print("NRF: SET_WRITE_PIPE_ADDR...")
                addr = bytesToIntArray(con.recv(5))
                if VERBOSE > 2:
                    print("NRF: SET_WRITE_PIPE_ADDR(" + str(addr) + ")")
                nRF2401.setWritePipeAddress(addr)

            elif cmd == NRF_GET_READ_PIPE_ADR:
                if VERBOSE > 3:
                    print("NRF: GET_READ_PIPE_ADDR...")
                pass

            elif cmd == NRF_GET_WRITE_PIPE_ADR:
                if VERBOSE > 3:
                    print("NRF: GET_WRITE_PIPE_ADDR...")
                pass

            elif cmd == NRF_FLUSH_TX:
                if VERBOSE > 2:
                    print("NRF: WRITE FLUSH TX...")
                nRF2401.writeFlushTX()

            elif cmd == NRF_FLUSH_RX:
                if VERBOSE > 2:
                    print("NRF: WRITE FLUSH RX...")
                nRF2401.writeFlushRX()

            elif cmd == NRF_POWER_UP:
                if VERBOSE > 2:
                    print("NRF: POWER UP...")
                nRF2401.powerUp()

            elif cmd == NRF_POWER_DOWN:
                if VERBOSE > 2:
                    print("NRF: POWER DOWN...")
                nRF2401.powerDown()

            elif cmd == NRF_SWITCH_TX:
                if VERBOSE > 2:
                    print("NRF: SWITCH_TX...")
                nRF2401.swithToTX()

            elif cmd == NRF_SWITCH_RX:
                if VERBOSE > 2:
                    print("NRF: SWITCH_RX...")
                nRF2401.swithToRX()

            elif cmd == NRF_RESET:
                if VERBOSE > 2:
                    print("NRF: RESET...")
                nRF2401.reset()

            elif cmd == NRF_SEND:
                if VERBOSE > 3:
                    print("NRF: SEND...")
                size = ord(con.recv(1))
                if VERBOSE > 3:
                    print("NRF: SEND(" + str(size) + ")...")
                data = bytesToIntArray(con.recv(size))
                if VERBOSE > 2:
                    print("NRF: SEND(" + str(data) + ")")
                res = nRF2401.sendData(data)
                returnBoolean(res)

            elif cmd == NRF_RECEIVE:
                if VERBOSE > 3:
                    print("NRF: RECEIVE...")
                size = ord(con.recv(1))
                if VERBOSE > 2:
                    print("NRF: RECEIVE(" + str(size) + ")")
                data = nRF2401.receiveData(size)
                if VERBOSE > 3:
                    print("NRF: RECEIVE(" + str(size) + ")=" + str(data))
                con.send(intArrayToBuffer(data))
            elif cmd == NRF_START_LISTENING:
                if VERBOSE > 2:
                    print("NRF: START_LISTENING...")
                nRF2401.startListening()
            elif cmd == NRF_STOP_LISTENING:
                if VERBOSE > 2:
                    print("NRF: STOP_LISTENING...")
                nRF2401.stopListening()
            elif cmd == NRF_POOL_DATA:
                if VERBOSE > 3:
                    print("NRF: POOL_DATA...")
                timeout = struct.unpack("f", con.recv(4))[0]
                if VERBOSE > 2:
                    print("NRF: POOL_DATA(" + str(timeout) + ")")
                res = nRF2401.poolData(timeout)
                if VERBOSE > 3:
                    print("NRF: POOL_DATA=" + str(res))
                returnBoolean(res)

            elif cmd == NRF_SEND_AND_RECEIVE:
                if VERBOSE > 3:
                    print("NRF: SEND_AND_RECEIVE...")
                timeout = struct.unpack("f", con.recv(4))[0]
                if VERBOSE > 3:
                    print("NRF: SEND_AND_RECEIVE(, " + str(timeout) + ")")
                size = ord(con.recv(1))
                if VERBOSE > 3:
                    print("NRF: SEND_AND_RECEIVE(" + str(size) + ")...")
                data = bytesToIntArray(con.recv(size))
                if VERBOSE > 2:
                    print("NRF: SEND_AND_RECEIVE(" + str(data) + ", " + str(timeout) + ")", flush=True)

                res = nRF2401.sendAndReceive(data, timeout)

                if VERBOSE > 3:
                    print("NRF: SEND_AND_RECEIVE()=" + str(res), flush=True)

                buf = intArrayToBuffer(res)

                if VERBOSE > 4:
                    print("NRF: SEND_AND_RECEIVE()=buf=" + str(buf), flush=True)
                con.send(buf)

            else:
                print("Unknown command " + str(cmd))

            # print("", end="", flush=True)

        spi = spidev.SpiDev()

        try:
            exit = False
            while not exit:
                if VERBOSE > 4:
                    print("Waiting on command")

                try:
                    cmd = ord(con.recv(1))
                    processCommand(cmd)
                except TypeError as ignore:
                    if VERBOSE > 3:
                        print("Got type error, leaving")
                    exit = True

        except ConnectionResetError as ignore:
            if VERBOSE > 4:
                print("Got connection reset error")
            pass

    def listen():
        try:
            while True:
                try:
                    con, addr = s.accept()
                    t = threading.Thread(target=session, args=[con])
                    t.daemon = True
                    t.start()
                except Exception as e:
                    print(str(e) + "\n" + ''.join(traceback.format_tb(e.__traceback__)))
        except KeyboardInterrupt as ki:
            print(" - Stopping")

    # thread = threading.Thread(target=listen)
    # thread.daemon = True
    # thread.start()

    listen()

try:
    startListen()
finally:
    s.close()
