#!/usr/bin/python3
from typing import Final
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())   # find .env file
import os


##### DATABASE FIELDS AND CONSTANTS #####

class Database:
    # convert fields from database to useful program names
    KEY_FIELD: Final[dict[str, str]] = {"Vznos": "payment",
                 "IP": "ip",
                 "Masck": "mask",
                 "Gate": "gateway",
                 "switchP": "switch",
                 "PortP": "port",
                 "dhcp_type": "dhcp",
                 "Add_IP": "public_ip",
                 "Number_serv": "nserv",
                 "Number_net": "nnet",
                 "Street": "street",
                 "House": "house"}
    
    # usernum field name
    USERNUM: Final[str] = "Number"


##### CONSTANTS FOR CITY SWITCH DIAGNOSTICS #####

class CitySwitch:
    # types of cli to identify model
    CLI_TYPES: Final[list[str]] = ["d-link", "cisco"]



##### PACKET SCANNING CONSTANTS #####

class PacketScan:
    # pipe for packet scanning path
    PIPE: Final[str] = os.getenv("PIPE")
