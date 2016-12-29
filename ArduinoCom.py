#!/usr/bin/env python3

import os
import types

from cmd2 import Cmd, options, make_option

from rip.head.spine.core import get_spine

from rip.head.spine.appendages.motor import Motor as SpineMotor

from appendages.motor import Motor as ACMotor

CURRENT_ARDUINO_CODE_DIR = "/Robot/CurrentArduinoCode"

class ArduinoCom(Cmd):
    intro = "Welcome to ArduinoCom. Type help or ? for commands.\nCtrl-D to exit."
    prompt = "AC> "
    doc_header = "Documentation available for:"
    undoc_header = "Not documented:"
    gs = None
    s = None

    def __init__(self):
        super().__init__()
        self.registeredDevices = [d for d in os.listdir(CURRENT_ARDUINO_CODE_DIR)
            if os.path.isdir("{0:s}/{1:s}".format(CURRENT_ARDUINO_CODE_DIR, d)) and
            not d == ".git" and os.path.exists("{0:s}/{1:s}/{1:s}.json"
                                               .format(CURRENT_ARDUINO_CODE_DIR, d))]
        self.connectedDevices = [d for d in self.registeredDevices 
                                 if os.path.exists("/dev/{0:s}".format(d))]


    def do_connect(self, parseResults):
        args = parseResults.parsed[1].split()
        if len(args) != 1:
            self.help_connect()
            return
        arduinoName = args[0]

        if arduinoName not in self.connectedDevices:
            print("Arduino \"{}\" is not available.".format(arduinoName))
            return

        self.gs = get_spine(devices=[arduinoName])
        self.s = self.gs.__enter__()
        self.appendages = self.s.get_appendage_dict()

        for name, appendage in self.appendages.items():
            if isinstance(appendage, SpineMotor):
                self.__dict__["do_" + name] = types.MethodType(ACMotor.interact, self)
                self.__dict__["help_" + name] = types.MethodType(ACMotor.help, self)
                self.__dict__["complete_" + name] = types.MethodType(ACMotor.complete, self)


    def help_connect(self):
        print("usage: connect <ArduinoName>")

    def complete_connect(self, text, line, begidx, endidx):
        return [i for i in self.connectedDevices if i.startswith(text)]

    def do_disconnect(self, parseResults):
        if self.gs is not None:
            self.gs.__exit__(None, None, None)
            self.s = None
            self.gs = None

    def do_exit(self, parseResults):
        self.do_disconnect(None)
        return True
    
    def do_quit(self, parseResults):
        return self.do_exit(parseResults)

    def do_EOF(self, parseResults):
        print()
        return self.do_exit(parseResults)
    do_eof = do_EOF

    def get_names(self):
        return dir(self)

if __name__ == '__main__':
    ac = ArduinoCom()
    ac.debug = True
    ac.cmdloop()
