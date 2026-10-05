#!/usr/bin/env python3
"""
vrc_osc_watch.py

Watch incoming VRChat OSC messages in the terminal.

VRChat's default OSC output port is 9001.

Install:
    py -m pip install python-osc

Run:
    py vrc_osc_watch.py
"""

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer

HOST = "127.0.0.1"
PORT = 9001


def show_message(address, *args):
    if args:
        values = " ".join(repr(value) for value in args)
        print(f"{address:<45} {values}")
    else:
        print(address)


dispatcher = Dispatcher()
dispatcher.set_default_handler(show_message)

print("vrc osc watch")
print("─────────────")
print(f"listening on {HOST}:{PORT}")
print("press Ctrl+C to stop")
print()

server = BlockingOSCUDPServer((HOST, PORT), dispatcher)

try:
    server.serve_forever()
except KeyboardInterrupt:
    print("\n⊹ stopped")
finally:
    server.server_close()
