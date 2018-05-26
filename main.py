from NaiveBayes import NaiveBayes
import os
import sys
import json as json
import menus
import tkinter
from tkinter import filedialog


class MenuClass:
    def __init__(self, nb):
        self.loaded_model = False
        self.nb = nb

    def clearAllTheThings(self):
        """Clears command prompt in win & ios"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_state_menu(self):
        """Prints menu """
        self.clearAllTheThings()

        if nb.train_loaded:
            print("TRAINING DATA LOADED")
        else:
            print("TRAINING DATA NOT LOADED")

        if nb.test_loaded:
            print("TEST DATA LOADED")
        else:
            print("TEST DATA NOT LOADED")

        if nb.train_loaded:
            print(menus.start_menu_trained)
        else:
            print(menus.start_menu)


        

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

            elif input_v == "loadtest" or input_v == "3":
                self.nb.load_test_folder()
            
            elif input_v == "score" or input_v == "4":
                if not nb.train_loaded:
                    print("Training data not loaded")
                elif not nb.test_loaded:
                    print("Test data not loaded")
                else:
                    self.nb.score()
                input("Press enter to continue...")

            elif input_v == "classify" or input_v == "5":
                self.nb.classify()
                input("Press enter to continue...")

            elif input_v == "classifyfile" or input_v == "6":
                print("Select text file to classify")
                tkinter.Tk().withdraw()
                file_dir_path = filedialog.askopenfilename()
                with open(file_dir_path, "r") as data:
                    self.nb.classify(data.read())
                input("Press enter to continue...")

            elif input_v == "aboutus" or input_v == "7":
                print("""
                    Native Bais implemented by people
                    Candidates : 42, 31, 20.
                    """)
                input("Press enter to continue...")

            elif input_v == "save" or input_v == "8":
                if nb.is_not_loaded():
                    nb.print_load_model()
                    input("Press enter to continue...")
                self.nb.saveData()

            elif input_v == "exit" or input_v == "9":
                sys.exit()

            else:
                print("Unknown keyword or command, please try again!")

            


if __name__ == '__main__':
    nb = NaiveBayes()
    menu = MenuClass(nb)
    menu.prompt()
