from NaiveBayes import NaiveBayes
import os
import sys
import json as json

import tkinter
from tkinter import filedialog


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

class MenuClass:
    def __init__(self, nb):
        self.loaded_model = False
        self.menu = []
        self.nb = nb



        with open(os.path.join(__location__, "menus.json"), "r") as data:
            self.menu = json.load(data)

    def clearAllTheThings(self):
        """Clears command prompt in win & ios"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_state_menu(self):
        """Prints menu """
        self.clearAllTheThings()
        if nb.train_loaded:
            print("Model IS TRAINED!")
        else:
            print("Model IS NOT TRAINED")

        if nb.test_loaded:
            print("TEST DATA LOADED")
        else:
            print("TEST DATA NOT LOADED")
        print()

        for line in self.menu[0]:
            print(line)

    def prompt(self):
        """Awaits input from user, launces correct method based on response"""
        while True:
            self.print_state_menu()
            input_v = input("> ")
            self.clearAllTheThings()

            if not self.loaded_model and input_v == "generate" or input_v == "1":
                self.nb.loadData()

            elif not self.loaded_model and input_v == "import" or input_v == "2":
                self.nb.load_data_from_file()

            elif input_v == "score" or input_v == "3":
                if not nb.train_loaded:
                    print("Training data not loaded")
                else:
                    self.nb.score()
                input("Press enter to continue...")

            elif input_v == "classify" or input_v == "4":
                self.nb.classify()
                input("Press enter to continue...")

            elif input_v == "classifyfile" or input_v == "5":
                if nb.is_not_loaded():
                    nb.print_load_model()
                    input("Press enter to continue...")
                    continue

                print("Select text file to classify")
                tkinter.Tk().withdraw()
                file_dir_path = filedialog.askopenfilename()
                with open(file_dir_path, "r") as data:
                    self.nb.classify(data.read())
                input("Press enter to continue...")

            elif input_v == "aboutus" or input_v == "6":
                print("""\n
                    Native Bais implemented by people
                    HME005,TPE044,EOS005
                    Hans, Thomas og Espen\n
                    """)
                input("Press enter to continue...")

            elif input_v == "save" or input_v == "7":
                if nb.is_not_loaded():
                    nb.print_load_model()
                    input("Press enter to continue...")
                    continue
                self.nb.saveData()

            elif input_v == "exit" or input_v == "8":
                sys.exit()

            else:
                print("Unknown keyword or command, please try again!")

            


if __name__ == '__main__':
    nb = NaiveBayes()
    menu = MenuClass(nb)
    menu.prompt()
