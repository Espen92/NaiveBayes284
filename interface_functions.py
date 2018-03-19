import os
import sys


# for å cleare på både mac å pc ..i think?
def print_inline(*args):
    print("".join(args))
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K")


def clearAllTheThings():
    """Clears command prompt in win & ios"""
    os.system('cls' if os.name == 'nt' else 'clear')


def help_menu(level):
    """Print selector for help menu"""
    if level == 0:
        print(get_menu(("load", "loads the data")))
    if level == 2:
        print(get_menu(("score", "scores based on the entire test set"),
                       ("class", "lets you input a review")))
    if level == 3:
        print(get_menu(("any text", "classifies your review")))


def get_menu(*commands):
    """
    Generere help menu med extra commands

    Keyword arguments:
    *commands - en iterable med toupler som holder på command navn, og description
    """
    commandsstr = ""
    for command, desc in commands:
        commandsstr += f"\n|   {command}            - {desc}"

    return f"""    --------------Help Menu---------
        | ctrl + c will stop the script. (os->windows)
        |
        |   Commands:      Explanation:
        |{commands}
        |   ----------------------------
        |   stop,
        |   kill,
        |   exit            - stops the script
        |   clear           - clears this window
        |   about           - about things
        |   help            - shows this
        --------------------------------
    """


def aboutus():
    print("""
    Native Bais implemented by people
    HME005,TPE044,EOS005
    Hans, Thomas og Espen
    """)
