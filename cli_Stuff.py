import os
import NaiveBayes as nb

myPotatoes = 0
list_ = []
i = 0


def plussPotato(i):
    global myPotatoes
    myPotatoes += i


def printPotato():
    print(f"number of potatoes {myPotatoes}")


# for å cleare på både mac å pc ..i think?
def clearAllTheThings():
    os.system('cls' if os.name == 'nt' else 'clear')


def help_menu(level):
    if level == 0:
        print("""    --------------Help Menu---------
        | ctrl + c will stop the script. (os->windows)
        |
        |   Commands:      Explanation:
        |   potato          - runs potato.
        |   load            - loads the data
        |   ----------------------------
        |   stop,
        |   kill,
        |   exit            - stops the script
        |   clear           - clears this window
        |   about           - about things
        |   help            - shows this
        --------------------------------""")
    if level == 1:
        print("""    --------------Help Menu---------
        | ctrl + c will stop the script. (os->windows)
        |
        |   Commands:      Explanation:
        |   any number      - add x potatoes
        |   ----------------------------
        |   stop,
        |   kill,
        |   exit            - stops the script
        |   clear           - clears this window
        |   about           - about things
        |   help            - shows this
        --------------------------------""")
    if level == 2:
        print("""    --------------Help Menu---------
        | ctrl + c will stop the script. (os->windows)
        |
        |   Commands:      Explanation:
        |   test            - runs a predefined test
        |   score           - scores based on the entire test set
        |   class           - lets you input a review
        |   ----------------------------
        |   stop,
        |   kill,
        |   exit            - stops the script
        |   clear           - clears this window
        |   about           - about things
        |   help            - shows this
        --------------------------------""")
    if level == 3:
        print("""    --------------Help Menu---------
        | ctrl + c will stop the script. (os->windows)
        |
        |   Commands:      Explanation:
        |   any text        - classifies your review
        |   ----------------------------
        |   stop,
        |   kill,
        |   exit            - stops the script
        |   clear           - clears this window
        |   about           - about things
        |   help            - shows this
        --------------------------------""")


def aboutus():
    print("""
    Native Bais implemented by people
    HME005,TPE044,etc..
    stuff...lalalala...
    a.a.a.aallflld
    """)


def stopAll():
    quit()
