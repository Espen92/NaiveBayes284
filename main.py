from interface_functions import help_menu, clearAllTheThings, aboutus
from NaiveBayes import NaiveBayes
import NaiveBayesFunctions
from collections import Counter
import math
import os
import numpy as np
import json as json


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

class MenuClass:
    def __init__(self, nb):
        self.state = 0
        self.nb = nb
        self.prompt()

    def print_state_menu(self):
        with open(os.path.join(__location__,"menus.json"), "r") as data:
            j_data = json.load(data)
            for line in j_data[self.state]:
                print(line)

    def prompt(self, **kwargs):
        self.print_state_menu()
        input_v = input("> ")

        if input_v == "1":
            self.go_state_1()
        elif input_v == "2":
            self.go_state_2()
        elif input_v == "3":
            self.go_state_3()

    def go_state_1(self):
        pass

    def go_state_2(self):
        pass

    def go_state_3(self):
        pass


if __name__ == '__main__':
    clearAllTheThings()
    nb = NaiveBayes()
    menu = MenuClass(nb)
    menu.prompt()
