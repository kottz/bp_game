import random
import os
import time
import asyncio
#import relay

class Game:

    def __init__(self, p1, p2, p3, p4):
        self.running = False
        self.playerArray = [p1, p2, p3, p4]
        self.activeLight = 0
        self.winner = None
        self.winnerLight = None
        self.drinkEvent = asyncio.Event()        
        #Stages defined as intro, game, drink, win (1,2,3,4)
        self.currentStage = "intro"

        self.heartBeat = False
        self.observers = []

    def to_dict(self):
        return {'running': self.running,
               'players': self.playerArray,
               'winner': self.winner,
               'lights': self.activeLight,
               'stage': self.currentStage,
               'heartBeat': self.heartBeat}
    
    def attach(self, observer):
        self.observers.append(observer)

    def notify(self):
        for observer in self.observers:
            observer.update(self)
            
    def initGame(self):

        self.winner = self.calculateWinner()
        self.winnerLight = self.playerArray.index(self.winner)
        
        if(self.heartBeat):
            self.timeGap = 4
        else:
            self.timeGap = 2


    def calculateWinner(self):

        winner = random.choice(self.playerArray)
        while(winner == None):
            winner = random.choice(self.playerArray)

        return winner


    async def runGame(self):
        
        ###Intro
        self.running = True 
        self.currentStage = "intro"
        self.initGame()
        self.notify()
        
        #introLjusShow
        for i in range(12):
            self.activeLight = i%4
            self.notify()
            await asyncio.sleep(0.4)
        await asyncio.sleep(5.313)        
        ###Game
        self.currentStage = "game"
       
       #Light Sequence
        i = random.randint(10,25)
        while(i > 0):
            if(i == 1):
                self.activeLight = self.playerArray.index(self.winner)
            else:
                prev = self.activeLight
                self.activeLight = self.playerArray.index(random.choice([x for x in self.playerArray if x != self.playerArray[prev] and x != None]))
            i -= 1
            self.notify()
            await asyncio.sleep(self.timeGap)

        ###Drink
        self.currentStage = "drink"
        self.notify()

        #input("Tryck Enter när personen druckit upp!")
        self.drinkEvent.clear()
        await self.drinkEvent.wait()
        self.drinkEvent.clear()

        ###Win
        self.currentStage = "win"
        self.notify()
        await asyncio.sleep(8)
        
        ###End
        self.currentStage = "end"
        self.notify()
        self.running = False
        
class TextView:

    initialized = False
    prevStage = ""

    def update(self, subject):
        
        if(subject.currentStage != self.prevStage):
            self.prevStage = subject.currentStage
            if(subject.currentStage == "intro"):
                print("Winner is: " + subject.winner)
            print("--- CURRENT STAGE: " + subject.currentStage + " ---")
        else:
            print(" Active light: "+str(subject.activeLight))


class MusicView:
    initialized = False
    prevStage = ""

    def __init__(self, player):
        self.player = player
        self.introMusic = None
        self.gameMusic = None
        self.drinkMusic = None
        self.winMusic = None

    def update(self, subject):
       
        if(not self.initialized):
            self.introMusic = os.path.join("music","newGame.wav")
            if(subject.heartBeat):
                self.gameMusic = os.path.join("music", "heartbeat.opus")
            else:
                self.gameMusic = os.path.join("music","gameMusicLevel1.opus")
            self.drinkMusic = os.path.join("music", "drink", "bp_drinkMusic_"+subject.winner+".wav")
            self.winMusic = os.path.join("music", "winMusic.wav")
            self.initialized = True
            self.player.pause = False

        
        if(subject.currentStage != self.prevStage):
            self.prevStage = subject.currentStage
            if(subject.currentStage == "intro"):
                self.player.play(self.introMusic)
            elif(subject.currentStage == "game"):
                self.player.play(self.gameMusic)
            elif(subject.currentStage == "drink"):
                self.player.play(self.drinkMusic)
            elif(subject.currentStage == "win"):
                self.player.play(self.winMusic)
            else:
                self.initialized = False

class LightView:

    def update(self, subject):
        relay.turnAllOff()
        relay.turnOn(subject.activeLight)

        if(subject.currentStage == "end"):
            relay.turnAllOff()



