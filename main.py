import vlc
from game import Game
from game import TextView
import os
#player = vlc.MediaPlayer("/home/edward/Music/Allen Stone/Brown Eyed Lover/Allen Stone - Brown Eyed Lover.aac")

testGame = Game('viktor', 'edward', 'anton', 'malva')
textView = TextView()
testGame.attach(textView)
testGame.initGame()

themePlayer = vlc.MediaPlayer(os.path.join("music","fullTheme.opus"))
themePlaying = False

def changeSettings():
    for i in range(4):
        namn = input("Skriv in namn på plats "+str(i)+": ")
        if(namn == ""):
            testGame.playerArray[i] = None
        else:
            testGame.playerArray[i] = namn
    testGame.initGame()

while(True):
    print("")
    print("")
    print("Meny options")
    print("1) Start Game")
    print("2) Edit Config")
    print("3) Play/Pause Theme")
    print("4) Toggle heartBeat"+"("+str(testGame.heartBeat)+")")
    print("5) print current setup")
    print("6) Quit")
    option = input("Enter your option: ")

    if(option == "1"):
        testGame.runGame()
    elif(option == "2"):
        changeSettings()
    elif(option == "3"):
        if(themePlaying):
            themePlayer.quit()
            themePlaying = False
        else:
            themePlayer.play(os.path.join("music","fullTheme.opus"))
            #themePlayer.play()
            themePlaying = True
    elif(option == "4"):
        testGame.heartBeat = not testGame.heartBeat
        testGame.initGame()
    elif(option == "5"):
        print(str(testGame.playerArray))
    else:
        break


    


