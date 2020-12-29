# MonopolyStatistics

This program is able to simulate a large number of dices throws in a monopoly. The purpose is to get the probability to be on each territory and to determine which one is the most worth it. It's taking account of :
* chance
* community chest
* go to jail case
* go to jail after a given number of doubles 

To use the program, you have to type :

python3 playMonopoly --> if you're running the python3 branch

python3 playMonopoly --> if you're running the master branch

The board game is based on the french version, if you're using an other one, you can change the cards and case in config.yml following your boardgame. You may also have to change the program if the “go to" card are different. You also can change the number of faces on your dices and the number of double in a row to go to prison.

The french version implemented in the programm is based using the followings parameters

Each effect card has one of this card_effect :

Chance card which operates a move : 16
* 1 : Step back 3 cases
* 2 : Go to rue de la paix
* 3 : Go to the most close gare * 3
* 4 : Go to the start 
* 5 : Go to jail
* 6 : Go to the most close service
* 7 : Go to avenue henrie martin
* 8 : Go to boulevard de belleville
* 9 : No effect * 7

Community chest which operates a move : 16
* 1 : Go to jail 
* 2 : Go to the start 
* 3 : No effect * 14

Each case has one of this case_effect

Type of "effect case" :
* 1 : Take a community chest card
* 2 : Pay income taxes
* 3 : Take chance card
* 4 : Prison visit
* 5 : Go to jail
* 6 : Free park
* 7 : Pay taxe on fortune
* 8 : Start


￼
