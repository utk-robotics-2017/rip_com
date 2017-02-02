#!/usr/bin/env python3


class Lcd:
    def interact(self, parseResults):
        def help(name):
            self.__dict__["help_" + name]()

        name = parseResults.parsed[0]
        args = parseResults.parsed[1].split()

        if len(args) == 0:
            help(name)

        elif args[0] == "write":
            if len(args) < 2:
                help(name)
                return
            self.message = " ".join(args[1:])
            print("Writing message to LCD: " + self.message)
            self.s.get_appendage(name).write(self.message)

        elif args[0] == "clear":
            self.s.get_appendage(name).clear()

        elif args[0] == "writepos":
            if len(args) < 3:
                help(name)
                return
            try:
                pos1 = int(args[1])
                pos2 = int(args[2])
            except ValueError as err:
                help(name)
                return
            self.s.get_appendage(name).setpos(pos1, pos2)
            if len(args) > 3:
                self.message = " ".join(args[3:])
                self.s.get_appendage(name).write(self.message)

        elif args[0] == "writeln":
            if len(args) < 2:
                help(name)
                return
            try:
                line = int(args[1])
            except ValueError as err:
                help(name)
                return
            self.s.get_appendage(name).setpos(line, 0)
            if len(args) > 2:
                self.message = " ".join(args[2:])
                self.s.get_appendage(name).write(self.message)

        else:
            help(name)

    def help(self):
        print("usage: <lcd:str> write <value:str>")
        print("       <lcd:str> clear")
        print("       <lcd:str> writeln <value:int> ?<value:str>")
        print("       <lcd:str> writepos <value:int> <value:int> ?<value:str>")

    def complete(self, text, line, begidx, endidx):
        return [i for i in ["write", "clear", "writepos", "writeln"] if i.startswith(text)]
