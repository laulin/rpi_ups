#! /usr/bin/env python3

import struct
import smbus
import sys

DEFAULT_DEVICE_ADDRESS = 0x36
REGISTER_VCELL_ADDRESS = 2
REGISTER_SOC_ADDRESS = 4

class RaspiUPSHatInterface:
    # this class manages the communication with a MAX17043. It used to 
    # read voltage and state of charge. 
    # Should not be tested (interface)
    def __init__(self, port, device_address=DEFAULT_DEVICE_ADDRESS):
        self._bus = smbus.SMBus(port)
        self._file = "/dev/i2c-{}".format(port)
        self._device_address = device_address

    def _read_word(self, address):
        # read a word on the device and correct the endianness

        read = self._bus.read_word_data(self._device_address, address)
        big_endian_data = struct.pack(">H", read)
        little_endian_data = struct.unpack("<H", big_endian_data)[0] 
        return little_endian_data

    def read_voltage(self):
        # this function gets the voltage from the MAX17043 and return the value in volt
        raw_value = self._read_word(REGISTER_VCELL_ADDRESS)
        voltage = (raw_value >> 4) * 0.00125
        return voltage

    def read_capacity(self):
        # this function gets the state of charge from the MAX17043 and return the value in percent
        raw_value = self._read_word(REGISTER_SOC_ADDRESS)
        capacity = raw_value/256.0
        return capacity

    def __str__(self):
        return "{0} @ {1:#x} (MAX17043) : {2:.2f} V, {3:.1f}% ".format(self._file, self._device_address, self.read_voltage(), int(self.read_capacity()))

