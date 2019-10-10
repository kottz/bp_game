import mpv
from game import Game
from game import TextView
from game import MusicView
from game import LightView
import os
import relay

def my_log(loglevel, component, message):
    print('[{}] {}: {}'.format(loglevel, component, message))

testGame = Game('viktor', 'edward', 'anton', 'malva')
textView = TextView()
player = mpv.MPV()
musicView = MusicView(player)

relay.initGPIO()
lightView = LightView()
testGame.attach(lightView)
testGame.attach(musicView)
testGame.attach(textView)
testGame.initGame()

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
#    print("4) Toggle heartBeat"+"("+str(testGame.heartBeat)+")")
    print("5) print current setup")
    print("6) Quit")
    option = input("Enter your option: ")

    if(option == "1"):
        testGame.runGame()
    elif(option == "2"):
        changeSettings()
    elif(option == "3"):
        if(player.pause):
            player.play(os.path.join("music","fullTheme.opus"))
            player.pause = False
        else:
            player.pause = True
    elif(option == "4"):
        testGame.heartBeat = not testGame.heartBeat
        testGame.initGame()
    elif(option == "5"):
        print(str(testGame.playerArray))
    else:
        relay.cleanup()
        player.terminate()
        player = ''
        break


    


