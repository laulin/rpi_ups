#! /usr/bin/env python3

# This script is used to monitor UPS and call an action (i.e a command) is a condition is raise.
# The action string is interpolated with 'capacity'.
#
# example :
# python3 watch_ups.py -t 1 -ops more -v 50 "date" -> display the date if the SOC is over 50% every second
# python3 watch_ups.py -t 10 -ops less -v 30 "echo 'still {capacity}%" -> display the capacity if the SOC is under 30% every 10 seconds
#
# Application : To monitor your board, you can start your watch at the boot. Modify the file /etc/rc.local 
# and add your line. For example :
# watch_ups -t 30 -ops less -v 5 "poweroff"
# Take care : in this case, your script will run as root !

from time import sleep
import argparse
import os
import sys

from raspi_ups_hat_interface import RaspiUPSHatInterface

def parse_args():
    parser = argparse.ArgumentParser(description='Watch Raspi UPS hat capacity and do action regarding the SOC. Designed by laulin')
    parser.add_argument('-i', '--interval', type=int, default=10, help='The loop time between two poll')
    parser.add_argument('-ops', '--operator', choices=['less', 'more'], help='Define the operator apply between the value and the SOC')
    parser.add_argument('-v', '--value', type=int,
                        help='Define the compared value with the SOC, in percent')
    parser.add_argument('action', help='Define what to do if the comparaison is true')
    return parser.parse_args()


def do_action(action, capacity):
    os.system(action.format(capacity=capacity))

def check_less_than(ups, value, action):
    capacity = ups.read_capacity()
    if capacity < value:
        do_action(action, capacity)


def check_more_than(ups, value, action):
    capacity = ups.read_capacity()
    if capacity > value:
        do_action(action, capacity)


if __name__ == "__main__":
    ups = RaspiUPSHatInterface(1)
    args = parse_args()

    while True:
        if args.operator == 'less':
            check_less_than(ups, args.value, args.action)
        elif args.operator == 'more':
            check_more_than(ups, args.value, args.action)

        sleep(args.interval)
