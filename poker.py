import os
from deuces import Card
from deuces import Evaluator
from deuces import Deck
import itertools
import random

class Player:
        name = "" #gave players a name for easier debugging
	money = 0
	curHand = []
	def __init__(self, startMoney, name):
		self.money = startMoney
                self.name = name
        def __repr__(self): #represented as their name
                return self.name
	def returnBestHand(self, board): #CHANGE THIS FUNCTION TO RETURN THE BEST HAND WHEN ASKED AT THE RIVER
		return board
	def callAI(self, state): #CHANGE THIS FUNCTION. NEVER REFERENCE OTHER PLAYER'S CARDS.
                #You are not allowed to cheat! (obviously)
                #e.g. If we see curState.players[x].curHand, that's unacceptable.
		raiseAmount = random.randint(0, 100)
		maxbid = max(raiseAmount, random.randint(0, 100))
		if maxbid > self.money: #do not remove
			maxbid = self.money
		if raiseAmount > self.money: #do not remove
			raiseAmount = self.money
		possibleActions = ["check", ["raise", raiseAmount]] #can only check or raise,
                #since only one action is processed. Fold if max bid is lower than the biggest raise.
		return [ possibleActions[random.randint(0,len(possibleActions) - 1)], maxbid ]

#Our Poker AI
#made it a subclass of Player
#so we can play it against the default Player and see it's better than random!
class OurPokerAI(Player):
        myeval = Evaluator()

        #rank all card combinations and return the best one
        def returnBestHand(self, board):
                cards = self.curHand + board
                all5cardcombos = itertools.combinations(cards, 5)
                bestcombo = []
                minimum = 7462 #worst (highest) hand rank
                for combo in all5cardcombos:
                        #Card.print_pretty_cards(bestcombo)
                        score = self.myeval.evaluate(list(combo), list())
                        #print(score)
                        if score < minimum:
                                minimum = score
                                bestcombo = combo
                #print("Best Combo:")
                #Card.print_pretty_cards(bestcombo)
                return bestcombo

        def callAI(self, state):
                #CHANGE THIS FUNCTION. NEVER REFERENCE OTHER PLAYER'S CARDS.
                #You are not allowed to cheat! (obviously)
                #e.g. If we see curState.players[x].curHand, that's unacceptable.

                #raiseAmount and maxbid are random by default
                raiseAmount = random.randint(0, 100)
		maxbid = max(raiseAmount, random.randint(0, 100))
                
                action = "" #"raise", "check", or "fold"
                
                #different strategies based on stage of the game?
                if (state.curStage == "preflop"):
                        #if preflop, rank 2 card hand somehow...
                        pass
                elif (state.curStage == "flop"):
                        #if flop, rank 5 card hand and calculate chance of success
                        
                        #rank percentage of hand (0.0-1.0 where 0.0 is the best and 1.0 is the worst)
                        #e.g. a hand in the 100th percentile is HORRIBLE
                        handRank = self.myeval.get_five_card_rank_percentage(self.myeval.evaluate(self.curHand, state.board))
                        #flip handRank so 100 percent is now the best hand
                        handRank = 1.0 - handRank
                        if (handRank < 0.1):
                                #if hand is in the bottom 30th percentile, fold
                                action = "fold"
                        elif (handRank >= 0.1 or handRank <= 0.2):
                                #if hand is in the 30th - 50th percentile, check with a maxbid of 50
                                maxbid = 100
                                action = "check"
                        elif (handRank >= 0.2):
                                #if hand rank is greater than the 50th percentile, raise an amount based on the rank
                                raiseAmount = int(handRank * 100)
                                #keep maxbid at 100 to stay in the hand if possible
                                maxbid = 100
                                action = "raise"
                elif (state.curStage == "turn"):
                        #if turn, rank 6 card hand and calculate chance of success
                        
                        #rank percentage of hand (0.0-1.0 where 0.0 is the best and 1.0 is the worst)
                        #e.g. a hand in the 100th percentile is HORRIBLE
                        handRank = self.myeval.get_five_card_rank_percentage(self.myeval.evaluate(self.curHand, state.board))
                        #flip handRank so 100 percent is now the best hand
                        handRank = 1.0 - handRank
                        if (handRank < 0.1):
                                #if hand is in the bottom 30th percentile, fold
                                action = "fold"
                        elif (handRank >= 0.1 or handRank <= 0.2):
                                #if hand is in the 30th - 50th percentile, check with a maxbid of 50
                                maxbid = 100
                                action = "check"
                        elif (handRank >= 0.2):
                                #if hand rank is greater than the 50th percentile, raise an amount based on the rank
                                raiseAmount = int(handRank * 100)
                                #keep maxbid at 100 to stay in the hand if possible
                                maxbid = 100
                                action = "raise"
                elif (state.curStage == "river"):
                        #if river, rank 7 card hand and calculate chance of success
                        
                        #rank percentage of hand (0.0-1.0 where 0.0 is the best and 1.0 is the worst)
                        #e.g. a hand in the 100th percentile is HORRIBLE
                        handRank = self.myeval.get_five_card_rank_percentage(self.myeval.evaluate(self.curHand, state.board))
                        #flip handRank so 100 percent is now the best hand
                        handRank = 1.0 - handRank
                        if (handRank < 0.1):
                                #if hand is in the bottom 30th percentile, fold
                                action = "fold"
                        elif (handRank >= 0.1 or handRank <= 0.2):
                                #if hand is in the 30th - 50th percentile, check with a maxbid of 50
                                maxbid = 100
                                action = "check"
                        elif (handRank >= 0.2):
                                #if hand rank is greater than the 50th percentile, raise an amount based on the rank
                                raiseAmount = int(handRank * 100)
                                #keep maxbid at 100 to stay in the hand if possible
                                maxbid = 100
                                action = "raise"
                        
                #check to make sure you have enough money for maxbid and raiseAmount
                if maxbid > self.money: #do not remove
			maxbid = self.money
		if raiseAmount > self.money: #do not remove
		        raiseAmount = self.money

                #return actions
                if (action == "raise"):
                        return [["raise", raiseAmount], maxbid]
                elif (action == "check"):
                        return ["check", maxbid]
                elif (action == "fold"):
                        #print("Billy folds")
                        #checking with a maxbid of 0 is folding
                        return ["check", 0]
                else: #action == ""
                        #default: choose randomly
		        possibleActions = ["check", ["raise", raiseAmount]] #can only check or raise,
                        #since only one action is processed. Fold if max bid is lower than the biggest raise.
		        return [ possibleActions[random.randint(0,len(possibleActions) - 1)], maxbid ]

#holds state, you'll need to reference this in callAI
class State:
	stages = ["preflop", "flop", "turn", "river"]
	pot = 0
	curStage = ""
	players = []
	curPlayers = []
	board = []

	def __init__(self, players):
		self.players = players
	
#deal out cards to the board
def deal(cardAmt):
	draw = deck.draw(cardAmt)
	if isinstance(draw, int):
		curState.board.append(deck.draw(cardAmt))
	else:
		curState.board.extend(deck.draw(cardAmt))
	print("Board: ")
	Card.print_pretty_cards(curState.board) 

#get bet amounts from each player
def bet():
	actions = []
	maxRaise = 0
	for player in curState.curPlayers:
		action = player.callAI(curState)
		actions.append([player, action])
		if action[0][0] == "raise" and action[0][1] > maxRaise:
			maxRaise = action[0][1]
	for action in actions:
		if maxRaise > action[1][1]:
			curState.curPlayers.remove(action[0])
		else:
			action[0].money -= maxRaise 
			curState.pot += maxRaise
	print("Player Actions: " + str(actions))
	print("Pot: " + str(curState.pot))
	print("Current Players: ")
	for player in curState.curPlayers:
                print(player)
		print("   Hand: ")
		Card.print_pretty_cards(player.curHand)
		print("   Money: " + str(player.money))
                
#Setup for poker game
evaluator = Evaluator()
curPot = 0
players = [Player(2000, "Player1"), Player(2000, "Player2"), OurPokerAI(2000, "Billy")] #CAN CHANGE
print ("Players", players)
curState = State(players)

i = 0
while len(players) > 1:
        raw_input("Press Enter to continue...") #easier to debug when looking hand by hand
        print("")
        print("======== new hand ========")
	i += 1
	curState.pot = 0
	#ante
	for player in curState.players:
		ante = min(player.money, 50)
		player.money -= ante
		curState.pot += ante
	#prepare board and deck
	deck = Deck()
	deck.shuffle()
	curState.board = deck.draw(0)
	for player in curState.players:
		player.curHand = [] 
		player.curHand = deck.draw(2)
	#create players for this round
	curState.curPlayers = curState.players[:]
	#go through betting stages
	for stage in range(0, len(curState.stages)):
		curState.curStage = curState.stages[stage]
                print("======== " + curState.curStage + " ========")
		if curState.curStage == "flop":
			deal(3)
		elif curState.curStage == "turn":
			deal(1)
		elif curState.curStage == "river":
			deal(1)
		bet()
		#check if only one player is left
		if len(curState.curPlayers) == 1:
			print("Round Over")
			curState.curPlayers[0].money += curState.pot
			print("Winner: ")
                        print(curState.curPlayers[0])
			Card.print_pretty_cards(curState.curPlayers[0].curHand)
			print("New Stack: " + str(curState.curPlayers[0].money))
			break
		#If river check who won
		if curState.curStage == "river":
			print("Round Over")
			scores = []
			for player in curState.curPlayers:
                                #fixed this line so it actually evaluates hands and calculates scores
				scores.append(evaluator.evaluate(list(player.returnBestHand(curState.board)), list()))
                        #print (scores)
			winner = scores.index(min(scores))
			curState.curPlayers[winner].money += curState.pot
			print("Winner: ")
                        print(curState.curPlayers[winner])
			Card.print_pretty_cards(curState.curPlayers[winner].curHand)
			print("New Stack: " + str(curState.curPlayers[winner].money))
			break
	#remove broke players
	for player in curState.players:
		if player.money == 0:
			curState.players.remove(player)
                        
print(str(curState.players[0]) + " has won!")
