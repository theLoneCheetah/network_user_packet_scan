#!/usr/bin/python3
from typing import TypedDict
import pymysql.cursors
import os

# typed dict class for result of switch-port query
class SwitchPortData(TypedDict):
    switchP: str
    PortP: int


##### MAIN QUERIES #####

class Queries:
    GET_SWITCH_PORT = "SELECT switchP, PortP FROM users WHERE Number = %s"

##### CLASS TO GET DATA FROM THE DATABASE #####

class DatabaseManager:
    __SERVER: str
    __DATABASE: str
    __USER: str
    __PASSWORD: str
    __CHARSET: str
    __connection: pymysql.Connection
    
    # init data and connect to database
    def __init__(self) -> None:
        self.__SERVER = os.getenv("DB_SERVER")
        self.__DATABASE = os.getenv("DB_NAME")
        self.__USER = os.getenv("DB_USER")
        self.__PASSWORD = os.getenv("DB_PASSWORD")
        self.__CHARSET = os.getenv("DB_CHARSET")
        
        # start session
        self.__start_connection()
    
    # start
    def __start_connection(self) -> None:
        print("Connecting to database...")
        self.__connection = pymysql.connect(host=self.__SERVER,
                                            user=self.__USER,
                                            password=self.__PASSWORD,
                                            database=self.__DATABASE,
                                            charset=self.__CHARSET,
                                            cursorclass=pymysql.cursors.DictCursor)
        print("Success")
    
    # delete, close connection
    def __del__(self) -> None:
        print("Closing connection to database...")
        #self.__connection.close()
        print("Success")
    
    # get switch and port for user
    def get_switch_port(self, usernum: int) -> SwitchPortData:
        with self.__connection.cursor() as cursor:
            cursor.execute(Queries.GET_SWITCH_PORT, (usernum,))
            return cursor.fetchone()