#!/usr/bin/python3
from enum import Enum


##### CLASS FOR ERRORS' CODES #####

class ExceptionType(str, Enum):
    # base message
    BASE: str = "Невозможно продиагностировать "

    SWITCH_NOT_AVAILABLE: str = "L2: свитч недоступен"
    SWITCH_FREEZES: str = "L2: свитч зависает"
    SWITCH_CANNOT_CONNECT: str = "L2: не удаётся подключиться к свитчу, свитч пингуется"

    UNKNOWN_MODEL: str = "L2: неизвестная модель свитча с IP "


##### CLASS FOR USER'S EXCEPTION AND ERRORS' CODES #####

class MyException(Exception):
    __message: str
    __arg: str
    
    # init by base init and message
    def __init__(self, message: ExceptionType, arg: str = ""):
        super().__init__()
        
        # save message, add ip argument if unknown model error
        self.__message = message.value
        self.__arg = arg

    # print with base and specific messages concatenated
    def __str__(self) -> str:
        return ExceptionType.BASE.value + self.__message + self.__arg
    