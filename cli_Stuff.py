import os


def potato():
    for i in range(5):
        print(f"{i} potato")
        

def apple():
    for i in range(5):
        print(f"{i} apple")


#for å cleare på både mac å pc ..i think?
def clearAllTheThings():
    os.system('cls' if os.name=='nt' else 'clear')

def help_menu():
    print("""    --------------Help Menu---------
    | ctrl + c will stop the script. (os->windows)
    |
    |   Commands:      Explanation:
    |   potato          - runs potato.
    |   apple           - runs apple.
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