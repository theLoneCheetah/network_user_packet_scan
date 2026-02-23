#!/usr/bin/python3
from typing import TypeAlias, TypedDict

# alias for most of returned dictionaries
CommandRegexData: TypeAlias = dict[str, str]

# typeddist alias for show ports regex result
class ShowPortsCommandRegex(TypedDict):
    command: str
    regex: list[str]


##### SWITCH MODELS #####

# base_switches = {"DES-3028", "DES-3200-28", "DES-3526", "DGS-3000-24TC", "DGS-3200-24", "DGS-1210-28/ME", "DGS-3120-24TC"}

SWITCHES = {# L2
            "DES-3028": {"base_switch": "DES-3028", "ports": 28},
            "DES-3052": {"base_switch": "DES-3028", "ports": 52},
            "DES-3200-28": {"base_switch": "DES-3200-28", "ports": 28},
            "DES-3526": {"base_switch": "DES-3526", "ports": 26},
            "DGS-3000-24TC": {"base_switch": "DGS-3000-24TC", "ports": 24},
            "DGS-3000-26TC": {"base_switch": "DGS-3000-24TC", "ports": 24},
            "DGS-3200-24": {"base_switch": "DGS-3200-24", "ports": 24},
            "DGS-1210-28/ME": {"base_switch": "DGS-1210-28/ME", "ports": 28},
            "DGS-1210-52/ME": {"base_switch": "DGS-1210-28/ME", "ports": 52},
            # L2+
            "DGS-3120-24TC": {"base_switch": "DGS-3120-24TC", "ports": 24},
            # L3
            "DGS-3120-24SC": {},
            "DGS-3620-28TC": {},
            "DGS-3620-28SC": {},
            "DGS-3627G": {},
            "DGS-3630-28SC": {}}   # cisco-like
CISCO_SWITCH = "DGS-3630-28SC"


##### BASE COMMANDS #####

def show_model(cli_type: str) -> CommandRegexData:
    match cli_type:
        case "d-link":
            return {"command": "show switch",
                    "regex": r"Device Type\s+:\s+(?P<model>\S+)\s+.*Default Gateway\s+:\s+(?P<default_gateway>(\d{1,3}\.){3}\d{1,3})"}
        case "cisco":
            return {"command": "show version",
                    "regex": r"-+\s+1\s+(?P<model>\S+)\s+"}

def clipaging(model: str) -> CommandRegexData:
    match model:
        case x if x == CISCO_SWITCH:
            return {"disable": "terminal length 0",
                    "enable": "terminal length 24"}
        case _:
            return {"disable": "disable clipaging",
                    "enable": "enable clipaging"}


##### COMMANDS FOR L2 SWITCH #####

def show_packet(model: str, user_port: int) -> CommandRegexData:
    match model:
        case "DES-3028" | "DGS-1210-28/ME" | "DGS-3000-24TC" | "DES-3526" | "DGS-3120-24TC":
            return {"command": f"show packet ports {user_port}",
                    "regex": r"Total/(\d)?sec.*RX Bytes\s+\d+\s+(\d+).*TX Bytes\s+\d+\s+(\d+).*#"}
        case "DGS-3200-24" | "DES-3200-28":
            return {"command": f"show packet ports {user_port}",
                    "regex": r"Total/(\d)?sec.*RX Bytes\s+\d+\s+(\d+).*TX Bytes\s+\d+\s+(\d+).*CTRL"}
