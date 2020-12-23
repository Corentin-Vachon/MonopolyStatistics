# -*- coding: utf-8 -*-

import yaml
import random

class Game:     #TODO : define game var like : duration, nb of turn
    def __init__(self, config_game):
        self.nb_of_throw = config_game["nb_of_throw"]
        self.dice_faces = config_game["dice_faces"]
        self.double_to_go_to_prison = config_game["double_to_go_to_prison"]
        pass

    def __str__(self):
        return("A game has been launched : \n * "+str(self.nb_of_throw)+ " total of throws \n * "+ str(self.double_to_go_to_prison)+" double needed to go to prison \n * "+ str(self.dice_faces)+ " faces to the dice");

class BoardGame:         #TODO : for every cards, create a list
    def __init__(self, config_board_game):
        self.size = len(config_board_game) #nb of cases --> equal to the sum of cases
        self.list_of_case = []
        self.index = 0
        self.initialiseListOfCards(config_board_game)

    def initialiseListOfCards(self, config_board_game):     #TODO : sort the card by the order
        i = 0
        while i < (self.size):
            if (config_board_game[i].keys()[0] == "territory"):
                case = CaseTerritory(config_board_game[i].values()[0]) 
            elif (config_board_game[i].keys()[0] == "effect"):
                case = CaseEffect(config_board_game[i].values()[0]) 
            i += 1
            self.list_of_case.append(case)

    def __str__(self):
        for i in self.list_of_cards:
            return (i)

    def move(self, dice_score):
        #print("Nous sommes passés de : "+str(self.index%self.size)+" à "+str((self.index + dice_score)%self.size)+" avec un lancé de dés de :"+str(dice_score))
        self.index += dice_score
        card = self.list_of_case[self.index%self.size]
        if (card.type == "territory"):  
            card.arrived()
        elif  card.type == "effect" :
            if card.case_effect == 1:
                pass
            if card.case_effect == 1:
                pass
            if card.case_effect == 1:
                pass
            if card.case_effect == 1:
                pass
            if card.case_effect == 1:
                pass
            if card.case_effect == 1:
                pass
            if card.case_effect == 1:
                pass
            if card.case_effect == 1:
                pass

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
            return ("Case is : "+str(self.position)+" --> this is a territory")

class Card:
    def __init__(self, config_card):
        self.position = 1
        self.card_effect = config_card["card_effect"] # Each card_effect will be represented by a number
        pass

    def __str__(self):
        return (" Le type de la carte est : "+str(self.card_effect)+" sa position est "+str(self.position))

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
    game = Game(config["MonopolyStatistics"]["Rules"]["Game"])
    boardgame = BoardGame(config["MonopolyStatistics"]["Case"])
    card_stack_chance = CardStack(config["MonopolyStatistics"]["Cards"][0:len(config["MonopolyStatistics"]["Cards"])/2]) 
    card_stack_community_chest = CardStack(config["MonopolyStatistics"]["Cards"][len(config["MonopolyStatistics"]["Cards"])/2:len(config["MonopolyStatistics"]["Cards"])]) 
    i = 0
    while i < game.nb_of_throw:
        boardgame.move(throwDices())
        i += 1
    pass

def throwDices():    #TODO : generate 2 randint between 1 and 6
    dice1 = random.randint(1,6)
    dice2 = random.randint(1,6)
    dice = dice1 + dice2
    return dice
    if (dice1 == dice2): # gérer le passage en prison
        pass 
    pass

def movePlayer():    #TODO : change the position of the player
    pass

def getConfig():
    with open('config.yml') as file:
        return yaml.load(file, Loader=yaml.FullLoader)

if __name__ == "__main__":
    play()
