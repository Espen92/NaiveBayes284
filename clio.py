from cli_Stuff import *
import NaiveBayes as nb
import jupyter
import NaiveBayesFunctions
from collections import Counter
import math
import pathlib
import os
import numpy as np


# vurdere commands å kjører om input stemmer...


def doStuff(c, level):
    if (c == "exit" or c == "stop" or c == "kill"):
        quit()
    elif (c == "clear"):
        clearAllTheThings()
    elif (c == "help"):
        help_menu(level)
    elif (c == "about"):
        aboutus()
    elif ((level == 0)and(c == "potato")):
        level = 1
    elif ((level == 0)and(c == "load")):
        nb.loadData()
        level = 2
    elif ((level == 1)and(str.isdigit(c))):
        inp = int(c)
        plussPotato(inp)
        printPotato()
        level = 0
    elif ((level == 2)and(c == "score")):
        nb.score()
    elif ((level == 2)and(c == "test")):
        nb.myTest()
    elif ((level == 2)and(c == "class")):
        level = 3
    elif (level == 3):
        nb.classify(c)
        level = 2
    else:
        print("! Unrecognized command, please try \"help\" to see an overview of available commands.")
    return level


# lage en fin input thingy..


def commandy(level):
    if level == 1:
        print("How many potatoes?")
    print("")
    command = input("--> ")
    print("")
    level = doStuff(command, level)
    commandy(level)


clearAllTheThings()
print("\nPlease type a command or type \"help\" for alternatives")
commandy(0)
