import random
import os
import vlc
import time
#import relay_lib_seeed as relay

class Game:

    def __init__(self, p1, p2, p3, p4):

        self.playerArray = [p1, p2, p3, p4]
        self.activeLight = 0
        self.winner = None
        self.winnerLight = None


        self.introMusic = "some filepath"
        self.gameMusic = "some filepath"
        self.drinkMusic = "some filepath"
        self.winMusic = "some filepath"
        self.heartBeat = False
        self.observers = []
    
    def attach(self, observer):
        self.observers.append(observer)

    def notify(self):
        for observer in self.observers:
            observer.update(self)
            
            
    def initGame(self):

        self.winner = self.calculateWinner()
        self.winnerLight = self.playerArray.index(self.winner)
        
        namn = "viktor"
        #Sätt rätt parametrar för startmusik
        self.introMusic = os.path.join("music","newGame.wav")
        if(self.heartBeat):
            self.gameMusic = os.path.join("music", "heartbeat.opus")
            self.timeGap = 4
        else:
            self.timeGap = 2
            self.gameMusic = os.path.join("music","gameMusicLevel1.opus")

        self.drinkMusic = os.path.join("music", "drink", "bp_drinkMusic_"+self.winner+".wav")
        self.winMusic = os.path.join("music", "winMusic.wav")
    def calculateWinner(self):

        winner = random.choice(self.playerArray)
        while(winner == None):
            winner = random.choice(self.playerArray)

        return winner

    def runGame(self):
        print("Vinnaren är: "+self.winner)
        introPlayer = vlc.MediaPlayer(self.introMusic, "--aout=alsa")
        introPlayer.play()
        
        #Kör en introljusshow
        #for i in range(10):
         #   relay.relay_on(i%4 + 1) #lägger till 1 för att vi ska få 1-4
          #  time.sleep(0.4)
           # relay.relay_all_off()


        print ("vi prövar att starta första musiken")
        time.sleep(10.113) #Väntar in första introt
        #input("Väntar på knapptryck")


        gamePlayer = vlc.MediaPlayer(self.gameMusic)
        introPlayer.stop()
        gamePlayer.play()
        self.runLightSequence(self.timeGap)
        #input("väntar igen")

        drinkPlayer = vlc.MediaPlayer(self.drinkMusic)
        gamePlayer.stop()
        drinkPlayer.play()

        input("slut, väntar på input för att köra win")

        winPlayer = vlc.MediaPlayer(self.winMusic)
        drinkPlayer.stop()
        winPlayer.play()
        
        input("end")
        #relay.relay_all_off()

        #gör så att jag kör en input() så att jag kan se när de druckit färdigt. sen efter det kommer win-ljudet.

    def runLightSequence(self, timeGap):

        #first pick a random number of hops between two appropriate numbers, timeGap determines average gap between switches.
        hopNumber = random.randint(10, 25)
        previousLight = 0
        while(hopNumber > 0):
            if(hopNumber == 1): # Forces light on winner when hopnumber is 0. Game is rigged, already done. LightSequence just for show
                self.activeLight = self.winnerLight
            else:
                previousLight = self.activeLight
                newLight = random.randint(0,3)
                while(newLight == previousLight or self.playerArray[newLight] == None):
                    newLight = random.randint(0,3)
                self.activeLight = newLight 
            #relay.relay_all_off()
            #relay.relay_on(self.activeLight+1)
            hopNumber -= 1
            #print("active light: "+str(self.activeLight))
            self.notify()
            time.sleep(timeGap)

        return
    
class TextView:
    def update(self, subject):
        print("(tv) Active light: "+str(subject.activeLight))
