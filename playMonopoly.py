# -*- coding: utf-8 -*-

import yaml
import random
import matplotlib.pyplot as plt
import numpy as np

DEFINEIFPRINT = 0

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

class BoardGame:         # the brain of the program, it manages the progression of the player
    def __init__(self, config_board_game):
        self.size = len(config_board_game["Case"]) #40 in a classic monopoly
        self.list_of_case = []
        self.index = 0 #follow the progression of the player
        self.initialiseListOfCards(config_board_game["Case"])
        self.nb_of_double = 0 #if 3 nb_of_double --> player go to jail
        info_card = config_board_game["Rules"]["GameBoard"]

    def initialiseListOfCards(self, config_board_game):     #create a stack of card for both territory and effect cards
        i = 0
        while i < (self.size):
            if (list(config_board_game[i].keys())[0] == "territory"):
                case = CaseTerritory(list(config_board_game[i].values())[0]) 
            elif (list(config_board_game[i].keys())[0] == "effect"):
                case = CaseEffect(list(config_board_game[i].values())[0]) 
            i += 1
            self.list_of_case.append(case)

    def goTo(self, position): #used in target case effect
        return position

    def mostCloseGare(self): #return the position of the nearest gare
        value = 10 - ((self.index)%10 +5)
        if value > 0: return  value
        else : return value + 10

    def mostCloseService(self): #return the position of the nearest service
        if (self.index > 28 and self.index < 13):
            return 13
        else : return (28)

    def __str__(self):
        for i in self.list_of_cards:
            return (i)

    def move(self, card_stack_chance, card_stack_community_chest, game):  # change  the index according to the dice score and the effect card
        dice_score, isDouble = throwDices(game.dice_faces)
        self.index = (dice_score + self.index)%self.size
        case = self.list_of_case[self.index]
        if (DEFINEIFPRINT == 1) : print(" We are at position : "+str(self.index))
        case.arrived()
        if  case.type == "effect" : #first loop -> when we are on a new case effect, we are looking for what to do 
            if case.case_effect == 1: # we are on a a community chest
                card_case_effect = card_stack_community_chest.pullCard()
                if card_case_effect == 1:
                    self.index = self.goTo(10)
                    self.list_of_case[self.index].arrived()
                    if(DEFINEIFPRINT == 1):print(" *I'm in Jail : ", self.index)
                if card_case_effect == 2:
                    self.index = self.goTo(0)
                    self.list_of_case[self.index].arrived()
                    if(DEFINEIFPRINT == 1):print(" *I'm to the start case : ", self.index)
                if card_case_effect == 3:
                    pass
            if case.case_effect == 2: # we pay taxes
                pass
            if case.case_effect == 3: # we take a chance
                card_case_effect = card_stack_chance.pullCard()
                if card_case_effect == 1: #step back 3 cases
                    self.index -= 3
                    self.list_of_case[self.index].arrived()
                    if(DEFINEIFPRINT == 1):print(" *I go back 3 cases ", self.index)
                if card_case_effect == 2: #go to rue de la paix
                    self.index = self.goTo(39)
                    self.list_of_case[self.index].arrived()
                    if(DEFINEIFPRINT == 1):print(" *I'm now at Rue de la Paix : ", self.index)
                if card_case_effect == 3: #most close gare
                    self.index = (self.index + self.mostCloseGare())%self.size
                    self.list_of_case[self.index].arrived()
                    if(DEFINEIFPRINT == 1):print(" *I'm to the nearest gare : ", self.index)
                if card_case_effect == 4: #go to begining
                    self.index = self.goTo(0)
                    self.list_of_case[self.index].arrived()
                    if(DEFINEIFPRINT == 1):print(" *I'm to the start case : ", self.index)
                if card_case_effect == 5: #go to jail
                    self.index = self.goTo(10)
                    self.list_of_case[self.index].arrived()
                    if(DEFINEIFPRINT == 1):print(" *I'm in Jail : ", self.index)
                if card_case_effect == 6: # most close service
                    self.index = self.mostCloseService()
                    self.list_of_case[self.index].arrived()
                    if(DEFINEIFPRINT == 1):print("Go to the nearest service : ", self.index)
                if card_case_effect == 7: #go to Henri Martin
                    if(DEFINEIFPRINT == 1):print(" *I'm now at Henri Martin : ", self.index)
                    self.index = self.goTo(24)
                    self.list_of_case[self.index].arrived()
                if card_case_effect == 8: #go to Belleville
                    self.index = self.goTo(11)
                    self.list_of_case[self.index].arrived()
                    if(DEFINEIFPRINT == 1):print(" *I'm now at Boulevard de Belleville : ", self.index)
                if card_case_effect == 9:
                    pass
            if case.case_effect == 4:
                pass
            if case.case_effect == 5: #go to jail
                self.index = self.goTo(10)
                self.list_of_case[self.index].arrived()
                if(DEFINEIFPRINT == 1):print(" *I'm in Jail : ", self.index)
            if case.case_effect == 6:
                pass
            if case.case_effect == 7:
                pass
            if case.case_effect == 1:
                pass
        if(isDouble):
            self.nb_of_double += 1
            if(self.nb_of_double == game.double_to_go_to_prison): #go to jail if we do double_to_go_to_prison doubles
                self.index = self.goTo(10) 
            else :
                self.move(card_stack_chance, card_stack_community_chest, game)
        else : 
            self.nb_of_double = 0

    def bilan(self, config): #prepare a list with  every  territory
        l = [x for x in self.list_of_case if x.type=="territory"]
        makeCamembert(l, config)

class Case: #generate every case of every kind
    def __init__(self, position, type):
        self.position = position
        self.occurs = 0
        self.type = type

    def __str__(self):
        return ("La case : "+str(self.position))

    def arrived(self): #when we arrived on the case, increment a counter
        self.occurs += 1

class CaseEffect(Case): #childen of Case focused on effect card
    def __init__(self, case_territory_config):
        Case.__init__(self, case_territory_config["position"], "effect")
        self.case_effect = case_territory_config["case_effect"] # Each case_effect_type will be represented by a number

    def __str__(self):
            return ("Case is : "+str(self.position)+" --> this is an effect")

class CaseTerritory(Case):    #childen of Case focused on territory
    def __init__(self, case_territory_config):
        Case.__init__(self, case_territory_config["position"], "territory")
        self.color = case_territory_config["color"] #color of the card
        self.display = case_territory_config["display"] #color of the card
        self.price = case_territory_config["price"] #Price of the hotel
        self.occurs = 0
        self.name = case_territory_config["name"]

    def __str__(self):
            return ("Case is : "+str(self.position)+ " --> this is a ** " +self.color+" ** territory and it occurs : "+str(self.occurs))

    def result(self):
        print("The territory color "+self.color+" appears :"+str(self.occur)+"and cost : "+str(self.price))

class Card: 
    def __init__(self, config_card): #represent each card
        self.position = 1
        self.card_effect = config_card["card_effect"] # Each card_effect will be represented by a number

    def __str__(self):
        return (" Card type is : "+str(self.card_effect)+" her position is "+str(self.position))

class CardStack:    #create buffer circular functions to simulate stack of cards
    def __init__(self, config_card_stack):
        self.size_stack = len(config_card_stack)
        self.list_of_cards = []
        self.type = list(config_card_stack[0].keys())[0]
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
        
    def pullCard(self): #pick a new card
        self.occur += 1
        return self.list_of_cards[self.occur%self.size_stack].card_effect

def play(): #handle the game
    config = getConfig()
    global DEFINEIFPRINT
    DEFINEIFPRINT = int(config["MonopolyStatistics"]["Config"]["print"])
    game = Game(config["MonopolyStatistics"]["Rules"]["Game"])
    boardgame = BoardGame(config["MonopolyStatistics"])
    card_stack_chance = CardStack(config["MonopolyStatistics"]["Cards"][0:int(len(config["MonopolyStatistics"]["Cards"])/2)]) 
    card_stack_community_chest = CardStack(config["MonopolyStatistics"]["Cards"][int(len(config["MonopolyStatistics"]["Cards"])/2):len(config["MonopolyStatistics"]["Cards"])]) 
    i = 0
    while i < game.nb_of_throw: #play the number of turn defined
        game.newTurn()
        boardgame.move(card_stack_chance, card_stack_community_chest, game)
        i += 1
    boardgame.bilan(config)
    pass

def throwDices(dice_faces):    #generate 2 randint between 1 and 6
    dice1 = random.randint(1,dice_faces)
    dice2 = random.randint(1,dice_faces)
    dice = dice1 + dice2
    isDouble = dice1 == dice2
    if DEFINEIFPRINT == 1: print( " dices said : "+str(dice))
    return dice, isDouble
    pass

def makeCamembert(l, config): #handle the display
    l.sort(key = lambda l: l.color)
    labels = [x.name for x in l ]
    sizes = [x.occurs for x in l ]
    colors = [x.color for x in l ]
    colors = [x if x != "gare" else "white" for x in colors ]
    colors = [x if x != "service" else "grey" for x in colors ]
    colors = [x if x != "blueligth" else "blue" for x in colors ]

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels,colors=colors,autopct = lambda x: str(round(x, 2)) + '%')
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()

    sizes_in, labels_in,colors_in = [], [], []
    for i in l:
        if i.color not in labels_in:
            labels_in.append(i.color)
            sizes_in.append(i.occurs)
            colors_in.append(i.color)
        else :
            sizes_in[len(sizes_in)-1] += i.occurs

    colors_in = [x if x!="gare" else "white" for x in colors_in]
    colors_in = [x if x!="service" else "grey" for x in colors_in]

    sizes_out, labels_out,colors_out = [], [], []
    sizes_out = [x.occurs for x in l ]
    colors_out = [x.display for x in l ]
    labels_out = [x.name for x in l ]

    fig, ax = plt.subplots()
    ax.axis('equal')
    width = 0.5

    pie, _ = ax.pie(sizes_out,  labels=labels_out, colors=colors_out)
    plt.setp( pie, width=width, edgecolor='white')

    pie2, _ = ax.pie(sizes_in, radius=1-width, labels=labels_in,labeldistance=0.7, colors=colors_in)
    plt.setp( pie2, width=width, edgecolor='white')
    plt.show()

def getConfig(): #read the config from the configuration file
    with open('config.yml') as file:
        return yaml.load(file, Loader=yaml.FullLoader)

if __name__ == "__main__":
    play()
