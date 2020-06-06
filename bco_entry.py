#!/usr/bin/env python3

import logging
import signal
import subprocess
import sys
import threading
import time

from collections import deque
from functools import partial

from pykeyboard import PyKeyboardEvent

class KeyboardListener(PyKeyboardEvent):
    def __init__(self, entry, log_name):
        PyKeyboardEvent.__init__(self)
        self.logger = logging.getLogger(log_name + ".keyboard")
        self.control_characters = {
            'BackSpace': lambda x: x.pop(),
            'Return': lambda x: flush_command(x),
            'Shift_L': lambda x: x,
            'Shift_R': lambda x: x
        }
        # self.logger.setLevel(logging.DEBUG)
        self.new_event = threading.Event()
        # self._reset_data()
        self.shift = False
        self.command = deque()

    # def _reset_data(self):
    #     self.event_data = {
    #         "presses": 0
    #     }

    def tap(self, keycode, character, press):
        # logging.debug("Clicked keycode: {}".format(keycode))
        # self.logger.info("Input received: {}, {}, {}".format(keycode, character, press))
        if press:
            if character in self.control_characters:
                self.control_characters[character](command)
            else:
                command.append(character)
        # self.logger.debug("Input received: {}, {}, {}".format(keycode, character, press))
        # self.event_data["presses"] += 1
        self.new_event.set()

    def escape(self, event):
        # Always returns False so that listening is never stopped
        return False

    def next_event(self):
        """Returns an event and prepares the internal state so that it can start to build a new event"""
        self.new_event.clear()
        return
        # data = self.event_data
        # # self._reset_data()
        # return data

    def has_new_event(self):
        return self.new_event.is_set()

def flush_command(command):

    # This should block while awaiting the return code (as if blocking while a command was entered)

    cmd = ''.join(list(command))
    while len(command) > 0:
        command.popleft()
    print("Caught command {}".format(cmd))
    # Starting a manager thread could be done here
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = None, None
    try:
        while proc.poll() is None:
            time.sleep(0.1)
            # Error handling logic can be put here
        output = [line.rstrip().decode('UTF-8') for line in proc.stdout.readlines()]
        err = [line.rstrip().decode('UTF-8') for line in proc.stderr.readlines()]
    except Exception as e:
        # More error handling logic can be here
        logger.error(f"Call {cmd} yielded an exception:\n\t{e}")
    if err is not None and err != []:
        logger.error(" ----- Found process error: -----")
        for line in err:
            if line:
                logger.error(f"{line}")
    if output is not None and output != []:
        logger.info(f"\t----- Output from command {cmd} (Return code {proc.returncode})-----")
        for line in output:
            if line:
                logger.info(f"{line}")

log_name = 'bco_capture'

logger = logging.getLogger(log_name)
logger.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
sh.setFormatter(formatter)
sh.setLevel(logging.DEBUG)
logger.addHandler(sh)

logger.info("BCO Capture, initialized")

command = deque()

key_listener = KeyboardListener(command, log_name)

def shutdown(keyboard, signal, frame):

    print("Interrupt recieved, shutting down")
    keyboard.stop()
    sys.exit()
    print("BCO keyboard shutdown, complete")

signal.signal(signal.SIGINT, partial(shutdown, key_listener))
signal.signal(signal.SIGTERM, partial(shutdown, key_listener))

key_listener.start()

print("Listener, starting...")
while True:
    time.sleep(1)
print("...Listener, shutting down")

key_listener.stop()
sys.exit()
