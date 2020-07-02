#from time import sleep
from cs1graphics import *
from cs1media import * 
import random
import csv

#######################################################
#######################################################
#######################################################

text_position_11 = (1000,200)
text_position_12 = (1000,300)
text_position_21 = (1000,600)
text_position_22 = (1000,700)
text_position_31 = (1500,200)
text_position_32 = (1500,300)

#######################################################
#######################################################
#######################################################

suit_names = ['Clovers', 'Diamonds', 'Hearts', 'Spades']
face_names = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']

card_size = (240, 360)
player_position = (200,300)
dealer_position = (200,700)
shift = 30 


#######################################################
#######################################################
#######################################################

record = []
information = []
now_game = 1
Game_try = 50
Turning_point = 10
sampling_number = 100
now_sampling = 0

def initialize():
    global now_game
    global bet_money
    global record
    global account 
    global now_sampling
    
    record = []
    now_game = 1
    bet_money = minimum_bet
    account = 0
    now_sampling += 1 


#######################################################
#######################################################
#######################################################

account = 0
bet_money = 1000
minimum_bet = 1000
maximum_bet = 300000


#######################################################
#######################################################
#######################################################


def most_frequent(the_list):

    dic = {}
    maxdic = 0 
    maxkey = 0  

    for i in range(len(the_list)):
        element = the_list.pop(0)
        if element in dic.keys():
            dic[element] += 1 
        else :
            dic[element] = 1 

    for key in dic: 
        if dic[key] > maxdic: 
            maxdic = dic[key]
            maxkey = key 
        elif dic[key] == maxdic: 
            if maxkey < dic[key]:
                maxkey = dic[key]
        else:
            pass

    return maxkey

#######################################################
#######################################################
#######################################################

class Card(object):

    def __init__(self,face,suit): 
    
        self.face = face
        self.suit = suit
        if self.suit == 'Diamonds' or self.suit == 'Hearts' :    
            self.color = "red"
        else :
            self.color = "black"
        self.state = True 

    def __str__(self):

        article = "a"
        if self.face == "Ace":
            article = "an "
        elif self.face == "Jack" or "Queen" or "King":
            article = "a "
        else : 
            article = ""

        return article + str(self.face) + "  of  " + self.suit
    
    def value(self, exception=False):
    
        try :
            #!        
            return int(self.face)
        except : 
            if self.face == "Ace" :
                if exception == True :
                    return 1 
                else :
                    return 11
            else :
                return 10

        
#######################################################
#######################################################
#######################################################


class deck(object):

    def __init__(self):
        self.cards = []

    def __len__(self):
        return len(self.cards)

    def clear(self):
        self.cards = []
    
    def add_pile(self,number=1):

        cards = []
        for i in range(number):
            for suit in suit_names:
                for face in face_names:
                    cards.append(Card(face, suit))
        random.shuffle(cards)
        self.cards = cards
    
    def hand(self):
        
        value_sum = 0 
        ace_deck = []
        
        for i in range(len(self)):
            value_sum += self.cards[i].value()
            if self.cards[i].face == "Ace":
                ace_deck.append(i)
            else:
                pass
        if value_sum > 21 and ace_deck != [] :
            value_sum = 0
            last_ace = ace_deck.pop()
            for i in range(len(self)):
                exception = (i==last_ace)
                value_sum += self.cards[i].value(exception)
        return value_sum
    
    def append(self,card):
        return self.cards.append(card)

    def pop(self):
        return self.cards.pop()

    def hand_but(self,number):

        new_deck = deck()
        new_deck.cards = self.cards
        for i in range(number):
            new_deck.pop()
        new_value = new_deck.hand()
        return new_value

#######################################################
#######################################################
#######################################################

game_switch = 1
betting_switch = 1 

def ask_yesno(prompt):

    key = input(prompt)
    while key == 'y' or key == 'n':
        if key == 'y':
            return True
        elif key == 'n':
            return False
        else :
            print("I beg your pardon!")

def game_strategy(player,dealer):

    global game_switch 
    if game_switch == 0:
        return ask_yesno("Hit = Press Y / Stay =  Press N")
    elif game_switch == 1:
        return game_strategy_1(player,dealer)
    elif game_switch == 2:
        return game_strategy_21(player,dealer,information)
    else :
        return game_strategy_22(player,dealer)

def betting_strategy(record):

    global betting_switch
    
    if record == [] or betting_switch == 0:
        return minimum_bet 
    elif betting_switch ==1 :
        return betting_strategy_1(record)
    else :
        return betting_strategy_2(record)


def game_strategy_1(player,dealer):

    switch = True 
    if 1 < dealer.cards[1].value() < 7:
        switch = False

    if player.hand() < 12: 
        return True 
    elif 11 < player.hand() < 17 and switch :
        return True  
    else:
        return False  

def game_strategy_21(player,dealer,information):

    global now_game

    player_worst , dealer_best = information 
    switch1 = 0 
    switch2 = False  
    switch3 = False    

    if now_game < 11: 
        return game_strategy_1(player,dealer)

    if 11 < player.hand() < 17: 
        switch1 = 1
    elif player.hand() > 16:
        switch1 = 2
    else:
        pass 

    if 1< dealer.cards[1] < 7:
        switch2 = True  
    if player.hand() >= player_worst :
        switch3 = True    
    if dealer.cards[1] < dealer_best:
        swtich2 = False 


    if switch1 == 1 and switch2 :
        return False 
    elif switch == 1 and switch3:  
        return False 
    elif switch1 == 2:
        return False 
    else :
        return True   

def betting_strategy_1(record):

    (winning_point,bet_money,account,player_info,dealer_info)=tuple(record[-1])
    
    if winning_point == "lose":
        bet_money *= 2
        if bet_money > maximum_bet:
            bet_money = maximum_bet
    elif winning_point == "win" :
        if bet_money == maximum_bet and account < maximum_bet:
            bet_money = maximum_bet
        else :
            bet_money = minimum_bet             
    else :
        pass
    return bet_money

def betting_strategy_2(record):
    if winning_point == "lose":
        bet_money *= 2
    elif winning_point == "win" :
        copy = record[:]
        copy.reverse()
        for i in range(len(copy)):
            if copy[i][0] =="lose":
                bet_money = minimum_bet
                break 
            else :
                continue
            
    else:
        pass
    return bet_money 

def Banking(winning_point,bet_money,account):
    if winning_point == "win":
        account += bet_money
    elif winning_point == "lose":
        account -= bet_money
    else :
        pass
    return account 


#######################################################
#######################################################
#######################################################

def print_on_canvas(prompt,location):

    x, y = location
    
    sentence = Text(prompt,50)
    sentence.setFontColor("white")
    sentence.setJustification('right')

    if location == text_position_31 or location == text_position_32:
        sentence.setFontColor("yellow")

    sentence.moveTo(x,y)
    black_board.add(sentence)

def game_regulator():

    global now_game

    if now_game < Game_try : 
        now_game += 1
        return True
    else:
        now_game = 0
        return False
        
def recording(record):

    global now_sampling
    player_info = []
    dealer_info = []
    total_winning = 0

    file_name = "strategy_" + str(now_sampling) +".csv" 
    with open(file_name, "wt", encoding = "utf-8" , newline ="") as csv_record:
        writer = csv.writer(csv_record)
        writer.writerow(["W/D/L","Betting","Account","Player_info","Dealer_info"])
        for line in record:
            writer.writerow(line)
            if line[0] == "win" :
                total_winning += 1
            elif line[0] == "lose":
                if 11< line[3]:
                    player_info.append(line[3])
                if line[4] < 7 :
                    dealer_info.append(line[4])
        writer.writerow(["Rate","Player_worst","Dealer_Lucky"])
        Rate = round(total_winning / len(record),3)
        Player_worst = most_frequent(player_info)
        Dealer_Lucky = most_frequent(dealer_info)
        writer.writerow([Rate,Player_worst,Dealer_Lucky])
    csv_record.close
    
def sub_record(information):

    return 0

#######################################################
#######################################################
#######################################################


def main_game():

    global bet_money
    global account

    table = deck()
    player = deck()
    dealer = deck()
    
    while True:

        bet_money = betting_strategy(record)
        print ("Welcome to Black Jack 101!\n")
        if len(table) < 12:
            table.add_pile()

        player.clear()
        dealer.clear()

        card = table.pop()
        player.append(card)
        print ("You are dealt :" + str(card))

        card = table.pop()
        card.state = False
        dealer.append(card)
        print ("Dealer is dealt a hidden card")

        card = table.pop()
        player.append(card)
        print ("You are dealt " + str(card))

        card = table.pop()
        dealer.append(card)
        print ("Dealer is dealt" + str(card))

        while player.hand() < 21 and game_strategy(player,dealer):
            card = table.pop()
            player.append(card)
            print ("You are dealt " + str(card))
    
        if player.hand() > 21:
            dealer.cards[0].state = True
            winning_point = "lose"
            
        else:
            print ("\nThe dealer's hidden card was " + str(dealer.cards[0]))
            while dealer.hand() < 17:
                card = table.pop()
                dealer.append(card)
                print ("Dealer is dealt " + str(card))
            dealer.cards[0].state = True

            if dealer.hand() > 21:
                winning_point = "win"
            else:
                if player.hand() > dealer.hand():
                    winning_point = "win"
                elif player.hand() < dealer.hand():
                    winning_point = "lose"
                else :
                    winning_point = "draw"


        player_sample = player.cards[:-1]
        account = Banking(winning_point,bet_money,account)
        record.append([winning_point,bet_money,account,player.hand_but(1),dealer.cards[1].value()])
        if not game_regulator():
            break
        if game_switch == 0 and (not ask_yesno("\nPlay another round? (y/n) ")):
            black_board.close()
            break
            

        
                    
#######################################################
#######################################################
#######################################################

for i in range(sampling_number):
    main_game()
    recording(record)
    initialize()

