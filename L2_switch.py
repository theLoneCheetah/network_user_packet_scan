#!/usr/bin/python3
# user's modules
from base_switch import BaseSwitch
import commands


##### CLASS TO COMMUNICATE WITH L2 SWITCH #####

class L2Switch(BaseSwitch):
    __user_port: str

    # L2 manager inits by user's port and base constructor
    def __init__(self, ipaddress: str, user_port: int, print_output: bool = False) -> None:
        super().__init__(ipaddress, "L2 switch", print_output)

        # user's port
        self.__user_port = user_port

        # save base model for further diagnosing
        self._model = commands.SWITCHES[self._model]["base_switch"]
    
    # get packages bytes on port
    def get_packets_port(self) -> tuple[int]:
        # command
        command_regex = commands.show_packet(self._model, self.__user_port)
        self._session.sendline(command_regex["command"])
        self._session.expect(command_regex["regex"])
        
        # save match and quit dynamic page on some switches
        match = self._session.match
        if self._model in {"DGS-3200-24", "DES-3200-28"}:
            self._quit_output()
        
        # return rx and tx bytes as integers
        return tuple(map(int, match.group(2, 3)))
