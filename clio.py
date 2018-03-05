from cli_Stuff import *


#vurdere commands å kjører om input stemmer...
def doThisPlease(c):
    if (c=="exit" or c=="stop" or c=="kill"):
        quit()
    elif (c=="clear"):
        clearAllTheThings()
    elif (c=="help"):
        help_menu()
    elif (c=="about"):
        aboutus()
    elif (c=="apple"):
        apple()
    elif (c=="potato"):
        potato()

    else:
        print("! Unrecognized command, please try \"help\" to see an overview of available commands.")

#lage en fin input thingy..
def commandy():
    print("")
    command = input("--> ")
    print("")
    doThisPlease(command)
    commandy()

clearAllTheThings()
print("\nPlease type a command or type \"help\" for alternatives")
commandy() 




