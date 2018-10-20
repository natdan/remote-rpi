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



class SMBus:
    def __init__(self, busNo):
        raise NotImplemented()

    def write_byte(self, i2cAddress, byte):
        raise NotImplemented()

    def write_byte_data(self, i2cAddress, localAddress, data):
        raise NotImplemented()

    def write_block_data(self, i2cAddress, localAddress, dataArray):
        raise NotImplemented()

    def read_byte(self, i2cAddress):
        raise NotImplemented()

    def read_byte_data(self, i2cAddress, localAddress):
        raise NotImplemented()

    def read_block_data(self, i2cAddress, localAddress):
        raise NotImplemented()

    def write_i2c_block_data(self, i2cAddress, localAddress, data):
        raise NotImplemented()

    def read_i2c_block_data(self, i2cAddress, localAddress, count):
        raise NotImplemented()
