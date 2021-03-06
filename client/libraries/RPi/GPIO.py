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


BOARD = 10
BCM = 11
SERIAL = 40
SPI = 41
I2C = 42
PWM = 43

NO_EDGE = 0
RISING_EDGE = 1
FALLING_EDGE = 2
BOTH_EDGE = 3

HIGH = 1
LOW = 0

PUD_OFF = 0
PUD_DOWN = 1
PUD_UP = 2


IN = None
OUT = None

FALLING = None
RISING = None
BOTH = None


def setwarnings(b):
    raise NotImplemented()


def setmode(mode):
    raise NotImplemented()


def input(pin):
    raise NotImplemented()


def output(pin, state):
    raise NotImplemented()


def setup(pin, type, pull_up_down=None):
    raise NotImplemented()


def cleanup():
    raise NotImplemented()


def add_event_detect(pin, edge, callback=None):
    raise NotImplemented()
