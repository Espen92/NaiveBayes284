from interface_functions import help_menu, clearAllTheThings, aboutus
from NaiveBayes import NaiveBayes
import NaiveBayesFunctions
from collections import Counter
import math
import os
import sys
import numpy as np
import json as json

import tkinter
from tkinter import filedialog


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

class MenuClass:
    def __init__(self, nb):
        self.nb = nb
        self.clearAllTheThings()
        self.prompt()

    def clearAllTheThings(self):
        """Clears command prompt in win & ios"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_state_menu(self):
        self.clearAllTheThings()
        with open(os.path.join(__location__,"menus.json"), "r") as data:
            j_data = json.load(data)
            for line in j_data[0]:
                print(line)

    def prompt(self):
        while True:
            self.print_state_menu()
            input_v = input("> ")

            if input_v == "generate" or input_v == "1":
                self.nb.loadData()

            elif input_v == "import" or input_v == "2":
                self.nb.load_data_from_file()

            elif input_v == "score" or input_v == "3":
                self.nb.score()
                input("Press enter to continue...")

            elif input_v == "classify" or input_v == "4":
                review = input("Give review to classify:")
                self.nb.classify(review)
                input("Press enter to continue...")

            elif input_v == "classifyfile" or input_v == "5":
                print("Select text file to classify")
                tkinter.Tk().withdraw()
                file_dir_path = filedialog.askopenfilename()
                with open(file_dir_path, "r") as data:
                    self.nb.classify(data.read())
                input("Press enter to continue...")

            elif input_v == "aboutus" or input_v == "6":
                input("Press enter to continue...")

            elif input_v == "save" or input_v == "7":
                self.nb.saveData()

            elif input_v == "exit" or input_v == "8":
                sys.exit()

            


if __name__ == '__main__':
    clearAllTheThings()
    nb = NaiveBayes()
    menu = MenuClass(nb)
    menu.prompt()
