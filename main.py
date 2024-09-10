import cv2
import pyautogui
import pydirectinput
import time
import socket
import random
from playsound import playsound

def matchTemplate(img, template):
    result = cv2.matchTemplate(img, template, cv2.TM_SQDIFF_NORMED)
    min_val = cv2.minMaxLoc(result)[0]
    thr = .05
    return min_val <= thr

def starterReset():
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(('localhost', 8888))
    clientsocket.send(b"Hello \n")
    shi = 0
    sockCheck = True
    while sockCheck:
        outMessage = clientsocket.recv(1024)
        shi = int(outMessage.decode('utf-8'))
        sockCheck = False
    clientsocket.close()
    if(shi < 70000): return False
    else: return True

def gameCheck():
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(('localhost', 8888))
    clientsocket.send(b"Hello \n")
    sockCheck = True
    tempGame = ""
    while sockCheck:
        outMessage = clientsocket.recv(1024)
        tempGame = str(outMessage.decode('utf-8')).replace("\n","").replace(" ","")
        print(tempGame + " detected.")
        sockCheck = False
    clientsocket.close()
    if("Ruby" in tempGame): return "Ruby"
    elif("Sapphire" in tempGame): return "Sapphire"
    elif("FireRed" in tempGame): return "Fire Red"
    elif("LeafGreen" in tempGame): return "Leaf Green"
    else: return ""

stream = True
sid = 99999
counter = 0
starter = starterReset()
rsStarter = "torchic"
frlgStarter = "bulbasaur"
if(starter): firstPass = False
else: firstPass = True
game = gameCheck()
sleepCount = 2
if(game == "Fire Red" or game == "Leaf Green"):
    template = cv2.imread("./assets/fightBox.png")
    starterTemplate = cv2.imread("./assets/starterBox" + frlgStarter.capitalize() + ".png")
elif(game == "Ruby" or game == "Sapphire"):
    template = cv2.imread("./assets/fightBoxRS.png")
    starterTemplate = cv2.imread("./assets/starterBoxRS.png")
    if(starter == "torchic"): sleepCount = 1.75
    else: sleepCount = 1.5

while(stream):
    sockCheck = True
    pyautogui.screenshot("test.png")
    time.sleep(sleepCount)
    if( not (starter and (game == "Fire Red" or game == "Leaf Green")) and matchTemplate(cv2.imread("test.png"),template)):
        counter = counter + 1
        print("Found a match. Checking for shiny roll.")
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect(('localhost', 8888))
        clientsocket.send(b"Hello \n")
        while sockCheck:
            outMessage = clientsocket.recv(1024)
            print("The shiny roll is " + str(outMessage.decode('utf-8')).replace("\n","") + ". This was attempt " + str(counter) + ".")
            sid = int(outMessage.decode('utf-8'))
            sockCheck = False
        clientsocket.close()
        if(sid < 8):
            playsound("./assets/shinysound.mp3",block=False)
            print("Congratulations! You have found a shiny!")
            time.sleep(5)
            stream = False  
        else:
            pydirectinput.keyDown("ctrl")
            pydirectinput.press("r")
            pydirectinput.keyUp("ctrl")
            if(not starter):
                pydirectinput.keyDown("enter")
                pydirectinput.press("left")
                pydirectinput.keyUp("enter")
            time.sleep(random.randrange(0,500)/100)
    elif(starter and (game == "Ruby" or game == "Sapphire") and rsStarter != "torchic" and matchTemplate(cv2.imread("test.png"),starterTemplate)):
        print("Starter box detected. Switching starters.")
        pydirectinput.press("x")
        if(rsStarter == "treecko"): pydirectinput.press("left")
        else: pydirectinput.press("right")
        pydirectinput.press("z")
    elif(starter and (game == "Fire Red" or game == "Leaf Green") and matchTemplate(cv2.imread("test.png"),starterTemplate)):
        print("Starter match found. Waiting for input, then running SID.")
        time.sleep(1.5)
        pydirectinput.press("z")
        time.sleep(1.5)
        pydirectinput.press("z")
        time.sleep(1.5)
        pydirectinput.press("z")
        counter = counter + 1
        print("Found a match. Checking for SID.")
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect(('localhost', 8888))
        clientsocket.send(b"Hello \n")
        while sockCheck:
            outMessage = clientsocket.recv(1024)
            print("The shiny ID is " + str(outMessage.decode('utf-8')).replace("\n","") + ". This was attempt " + str(counter) + ".")
            sid = int(outMessage.decode('utf-8'))
            sockCheck = False
        clientsocket.close()
        if(sid < 8):
            playsound("./assets/shinysound.mp3",block=False)
            print("Congratulations! You have found a shiny!")
            time.sleep(5)
            stream = False  
        else:
            pydirectinput.keyDown("ctrl")
            pydirectinput.press("r")
            pydirectinput.keyUp("ctrl")
            time.sleep(random.randrange(0,500)/100)
    else:
        print("Screenshot was not a match. Continuing.")
    if(firstPass):
        pydirectinput.keyDown("enter")
        pydirectinput.press("left")
        pydirectinput.keyUp("enter")
        firstPass = False
    if(stream):
        pydirectinput.press("z")
