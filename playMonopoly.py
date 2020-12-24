# -*- coding: utf-8 -*-

import yaml
import random
import matplotlib.pyplot as plt
import numpy as np


DEFINEIFPRINT = 1

class Game:     #TODO : define game var like : duration, nb of turn
    def __init__(self, config_game):
        self.nb_of_throw = config_game["nb_of_throw"]
        self.dice_faces = config_game["dice_faces"]
        self.double_to_go_to_prison = config_game["double_to_go_to_prison"]
        self.nb_of_turn = 0
        if(DEFINEIFPRINT == 1): print(self)
        pass

    def __str__(self):
        return("A game has been launched : \n * "+str(self.nb_of_throw)+ " total of throws \n * "+ str(self.double_to_go_to_prison)+" double needed to go to prison \n * "+ str(self.dice_faces)+ " faces to the dice");

    def newTurn(self):
        self.nb_of_turn += 1
        if(DEFINEIFPRINT == 1): print("A new turn begin : " + str(self.nb_of_turn))

class BoardGame:         #TODO : for every cards, create a list
    def __init__(self, config_board_game):
        self.size = len(config_board_game) #nb of cases --> equal to the sum of cases
        self.list_of_case = []
        self.index = 0
        self.initialiseListOfCards(config_board_game)
        self.nb_of_double = 0

    def initialiseListOfCards(self, config_board_game):     #TODO : sort the card by the order
        i = 0
        while i < (self.size):
            if (config_board_game[i].keys()[0] == "territory"):
                case = CaseTerritory(config_board_game[i].values()[0]) 
            elif (config_board_game[i].keys()[0] == "effect"):
                case = CaseEffect(config_board_game[i].values()[0]) 
            i += 1
            self.list_of_case.append(case)

    def goTo(self, position):
        return position #Positiond of the jail 

    def mostCloseGare(self):
        value = 10 - ((self.index)%10 +5)
        if value > 0: return  value
        else : return value + 10

    def mostCloseService(self):
        if (self.index > 29 and self.index < 13):
            return 13
        else : return (29)

    def __str__(self):
        for i in self.list_of_cards:
            return (i)

    def move(self, card_stack_chance, card_stack_community_chest):
        dice_score, isDouble = throwDices()
        self.index = (dice_score + self.index)%self.size
        card = self.list_of_case[self.index]
        if (DEFINEIFPRINT == 1) : print(" We are at position : "+str(self.index))
        if (card.type == "territory"):  
            card.arrived()
        elif  card.type == "effect" :
            if card.case_effect == 1: # Take a community chest
                card_case_effect = card_stack_community_chest.pullCard()
                if card_case_effect == 1:
                    self.index = self.goTo(11)
                    print(" *I'm in Jail : ", self.index)
                if card_case_effect == 2:
                    self.index = self.goTo(0)
                    print(" *I'm to the start case : ", self.index)
                if card_case_effect == 3:
                    pass
            if card.case_effect == 2:
                pass
            if card.case_effect == 3: # Take a chance
                card_case_effect = card_stack_chance.pullCard()
                if card_case_effect == 1:
                    self.index -= 3
                    print(" *I go back 3 cases ", self.index)
                if card_case_effect == 2: 
                    self.index = self.goTo(39)
                    print(" *I'm now at Rue de la Paix : ", self.index)
                if card_case_effect == 3: #most close gare
                    self.index += self.mostCloseGare()
                    print(" *I'm to the nearest gare : ", self.index)
                if card_case_effect == 4:
                    self.index = self.goTo(0)
                    print(" *I'm to the start case : ", self.index)
                if card_case_effect == 5:
                    self.index = self.goTo(11)
                    print(" *I'm in Jail : ", self.index)
                if card_case_effect == 6: # most close service
                    self.index = self.mostCloseService()
                    print("Go to the nearest service : ", self.index)
                if card_case_effect == 7:
                    print(" *I'm now at Henri Martin : ", self.index)
                    self.index = self.goTo(25)
                if card_case_effect == 8:
                    self.index = self.goTo(12)
                    print(" *I'm now at Boulevard de Belleville : ", self.index)
                if card_case_effect == 9:
                    pass
            if card.case_effect == 4:
                pass
            if card.case_effect == 5:
                self.index += self.goTo(11)
                print(" *I'm in Jail : ", self.index)
            if card.case_effect == 6:
                pass
            if card.case_effect == 7:
                pass
            if card.case_effect == 1:
                pass
        if(isDouble):
            self.nb_of_double += 1
            if(self.nb_of_double == 3):
                self.goTo(11)
            else :
                self.move(card_stack_chance, card_stack_community_chest)
        else : 
            self.nb_of_double = 0

    def bilan(self):
        l = [x for x in self.list_of_case if x.type=="territory"]
        makeCamembert(l)

class Case: #TODO : sum every occurences
    def __init__(self, position, type):
        self.position = position
        self.occurs = 0
        self.type = type
        pass

    def __str__(self):
        return ("La case : "+str(self.position))

    def arrived(self):
        self.occurs += 1

        pass

class CaseEffect(Case): #TODO : define type (chance, community), effect and target
    def __init__(self, case_territory_config):
        Case.__init__(self, case_territory_config["position"], "effect")
        self.case_effect = case_territory_config["case_effect"] # Each case_effect_type will be represented by a number

    def __str__(self):
            return ("Case is : "+str(self.position)+" --> this is an effect")

class CaseTerritory(Case):    #TODO : define color, average price and position
    def __init__(self, case_territory_config):
        Case.__init__(self, case_territory_config["position"], "territory")
        self.color = case_territory_config["color"] #color of the card
        self.price = case_territory_config["price"] #Price of the hotel
        self.occurs = 0
        pass

    def arrived(self):
        self.occurs += 1
        pass

    def __str__(self):
            return ("Case is : "+str(self.position)+ " --> this is a ** " +self.color+" ** territory and it occurs : "+str(self.occurs))

    def result(self):
        print("The territory color "+self.color+" appears :"+str(self.occur)+"and cost : "+str(self.price))

class Card:
    def __init__(self, config_card):
        self.position = 1
        self.card_effect = config_card["card_effect"] # Each card_effect will be represented by a number
        pass

    def __str__(self):
        return (" Card type is : "+str(self.card_effect)+" her position is "+str(self.position))

    def readCard(self):
        pass

class CardStack:    #TODO : create buffer circular functions to simulate stack of cards
    def __init__(self, config_card_stack):
        self.size_stack = len(config_card_stack)
        self.list_of_cards = []
        self.type = config_card_stack[0].keys()[0]
        self.initialiseStack(config_card_stack)
        self.occur = 0

    def initialiseStack(self, config_card_stack): # initialise a random stack of card
        i = 0
        while i < (self.size_stack):
            card = Card(config_card_stack[i][self.type])
            self.list_of_cards.append(card)
            i += 1
        random.shuffle(self.list_of_cards)
        j = 1
        for i in self.list_of_cards:
            i.position = j
            j += 1
        
    def pullCard(self):
        self.occur += 1
        return self.list_of_cards[self.occur%self.size_stack].card_effect

def play(): #handle the game
    config = getConfig()
    DEFINEIFPRINT = int(config["MonopolyStatistics"]["Config"]["print"])
    game = Game(config["MonopolyStatistics"]["Rules"]["Game"])
    boardgame = BoardGame(config["MonopolyStatistics"]["Case"])
    card_stack_chance = CardStack(config["MonopolyStatistics"]["Cards"][0:len(config["MonopolyStatistics"]["Cards"])/2]) 
    card_stack_community_chest = CardStack(config["MonopolyStatistics"]["Cards"][len(config["MonopolyStatistics"]["Cards"])/2:len(config["MonopolyStatistics"]["Cards"])]) 
    i = 0
    while i < game.nb_of_throw:
        game.newTurn()
        boardgame.move(card_stack_chance, card_stack_community_chest)
        i += 1
    boardgame.bilan()
    pass

def throwDices():    #TODO : generate 2 randint between 1 and 6
    dice1 = random.randint(1,6)
    dice2 = random.randint(1,6)
    dice = dice1 + dice2
    isDouble = dice1 == dice2
    if DEFINEIFPRINT == 1: print( " dices said : "+str(dice))
    return dice, isDouble
    pass

def makeCamembert(l):
    l.sort(key = lambda l: l.color)
    labels = [x.color for x in l ]
    sizes = [x.occurs for x in l ]
    colors = [x.color for x in l ]
    colors = [x if x != "gare" else "black" for x in colors ]
    colors = [x if x != "service" else "grey" for x in colors ]
    colors = [x if x != "blueligth" else "blue" for x in colors ]
    print(colors)
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels,colors=colors)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()

def getConfig():
    with open('config.yml') as file:
        return yaml.load(file, Loader=yaml.FullLoader)

if __name__ == "__main__":
    play()
