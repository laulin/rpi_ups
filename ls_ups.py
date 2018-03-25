#! /usr/bin/env python3

from raspi_ups_hat_interface import RaspiUPSHatInterface

if __name__ == "__main__":
    ups = RaspiUPSHatInterface(1)
    print(ups)