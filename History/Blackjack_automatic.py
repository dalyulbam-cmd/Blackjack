#from time import sleep
#from cs1media import * 
from cs1graphics import *
import random
import csv

"""
If we choose to bring images through cs1graphics.Image(), then
There is no necessary to use cs1media module above. 
"""

#######################################################
################## Text Image Location #####################
#######################################################

text_position_11 = (1000,200)
text_position_12 = (1000,300)
text_position_21 = (1000,600)
text_position_22 = (1000,700)
text_position_31 = (1500,200)
text_position_32 = (1500,300)

"""
text_position_11 lets you know the total value of player.
text_position_12 show whether player wins or loses
text_position_21 lets you know the total value of dealer.
text_position_22 show whether dealer goes over 21 and get bursted.
text_position_31 and 32 displays an amount of account and betting money.

"""

#######################################################
################## Basic Concepts #########################
#######################################################


suit_names = ['Clovers', 'Diamonds', 'Hearts', 'Spades']
face_names = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
black_board = Canvas(1800, 1000, 'dark green', 'Black Jack 101')

card_size = (240, 360)
player_position = (200,300)
dealer_position = (200,700)
shift = 30 


#######################################################
#################### Game operators #######################
#######################################################

now_game = 1
now_sampling = 0

###########################

record = []
information = []

Game_try = 30
Turning_point = 10
sampling_number = 100

###########################

def initialize():
    global now_game, bet_money, record, account, now_sampling, information

    information = []
    record = []
    now_game = 1
    bet_money = minimum_bet
    account = 0
    now_sampling += 1 

def game_regulator():

    global now_game

    if now_game < Game_try : 
        now_game += 1
        return True
    else:
        now_game = 0
        return False
        
#######################################################
####################### Money ##########################
#######################################################

"""
betting money takes infromation from document of Gangwon Land casino
"""

account = 0
bet_money = 1000
minimum_bet = 1000
maximum_bet = 300000

def Banking(winning_point,bet_money,account):
    if winning_point == "win":
        account += bet_money
    elif winning_point == "lose":
        account -= bet_money
    else :
        pass
    return account 

#######################################################
###################### Math ############################
#######################################################

"""
'most_frequent' function gets a list argument and
returns an element which is the most frequent in the elements and besides,
the biggest one among the most frequent.

It helps to find out which number is preferred by player. 
"""


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
################## Class : Card ############################
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
        # if an Ace card turns to the exception, then it counts as 1 not to 11. 
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
################# Class : Card Image ########################
#######################################################

"""
Consider a case that  didn't make Card_image class and
handle Layer() as instance attributes, It could be imagined that
there would be numorous attempts to build layers for locating cards. 

"""

class Card_Image(object):

    def __init__(self,card):
        # Information tranferred from Card class to Card_Image class...
        self.graphic = Layer()
        self.suit = card.suit
        self.face = card.face
        self.path = './image/'
        self.img = None
        self.state = card.state

    def __str__(self):
        return self.suit + "_" + str(self.face) + ".png"
    
    def draw(self):
        if self.state == True:
            self.img = Image(self.path+str(self))
        else :
            self.img = Image(self.path+"Back.png")
        self.graphic.add(self.img)


"""
draw_card function was designed to be remodeled after in case for
new challenge making... for example, 1:3 blackjack.
"""

def draw_card(player,dealer):

    black_board.clear()
    def sketch(someone,location):
        global card_distance
        for i in range(len(someone)):
            x, y = location
            x += i*shift
            card_paper = Card_Image(someone.cards[i])
            card_paper.draw()
            card_paper.graphic.moveTo(x,y)
            black_board.add(card_paper.graphic)

    sketch(player,player_position)
    sketch(dealer,dealer_position)
        
        

#######################################################
#################### Class : Deck ##########################
#######################################################

"""
It was truely uncomfortable to find some values written in those ways
    : hand_value(player.cards[:-1]), or 
    : dealer.cards.append(new_card)

So this class contains functions like __len__, append, pop to shorten sentences. 
    : hand_value(player.cards[:-1])  -> player.hand_but(1)
    : dealer.cards.append(new_card) -> dealer.append(new_card)
    
"""

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
        # build a 'new deck' declared by own class
        # and through away a few cards amount of the argument, number.
        new_deck = deck()
        new_deck.cards = self.cards
        for i in range(number):
            new_deck.pop()
        new_value = new_deck.hand()
        return new_value

#######################################################
##################### Strategy ###########################
#######################################################

game_switch = 2
betting_switch = 2 

#########################################
#########################################

def ask_yesno(prompt):

    key = input(prompt)
    while key == 'y' or key == 'n':
        if key == 'y':
            return True
        elif key == 'n':
            return False
        else :
            print("I beg your pardon!")

#########################################
#########################################


"""
Now, here are the switches for game strategies and betting strategies.

game_switch = 0 -> Input the True(hit) and False(Stay) by myself.
game_switch = 1 -> Automatic. It considers the hand value of player and dealer.
game_switch = 2 -> Automatic. It excludes the case frequently defeated before.

betting_switch = 0 -> Only minimum betting is allowed
betting_switch = 1 -> Martingale betting before the maximum betting
betting_swithc =2 -> Passionists. Consecutive winning bring the player to betting X5 

"""

def game_strategy(player,dealer):

    global game_switch 
    if game_switch == 0:
        return ask_yesno("Hit = Press Y / Stay =  Press N")
    elif game_switch == 1:
        return game_strategy_1(player,dealer)
    elif game_switch == 2:
        return game_strategy_21(player,dealer)
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


#########################################
#########################################


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

def game_strategy_21(player,dealer):

    global now_game
    global information 
    
    switch1 = 0 
    switch2 = False  
    switch3 = False    

    if now_game < 11: 
        return game_strategy_1(player,dealer)

    Player_worst = information[0]
    Dealer_Lucky = information[1]

    if 11 < player.hand() < 17: 
        switch1 = 1
    elif player.hand() > 16:
        switch1 = 2
    else:
        pass 

    if 1< dealer.cards[1].value() < 7:
        switch2 = True  
    if player.hand() >= Player_worst :
        switch3 = True    
    if dealer.cards[1].value() < Dealer_Lucky:
        swtich2 = False 


    if switch1 == 1 and switch2 :
        return False 
    elif switch1 == 1 and switch3:  
        return False 
    elif switch1 == 2:
        return False 
    else :
        return True   


#########################################

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

    (winning_point,bet_money,account,player_info,dealer_info)=tuple(record[-1])
    
    if winning_point == "lose":
        bet_money *= 2
        if bet_money > maximum_bet:
            bet_money = maximum_bet    
    elif  winning_point == "win":
        bet_money = minimum_bet
        if len(record) >1 and record[-2][0] == "win":
            bet_money = minimum_bet *5
        if bet_money >= maximum_bet and account < maximum_bet:
            bet_money = maximum_bet
    else:
        pass        
    return bet_money 

#######################################################
################ Message and information #####################
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
    
def sub_recording(record):

    player_info = []
    dealer_info = []
    
    for data in record:
        if data[0] == "lose":
            if 11< data[3] :
                player_info.append(data[3])
            if data[4] < 7 :
                dealer_info.append(data[4])        
    Player_worst = most_frequent(player_info)
    Dealer_Lucky = most_frequent(dealer_info)
        
    return [Player_worst,Dealer_Lucky]

#######################################################
################## Main game operator ######################
#######################################################


def main_game():

    global bet_money
    global account
    global information 

    table = deck()
    player = deck()
    dealer = deck()
    
    while True:

        bet_money = betting_strategy(record)
        print ("Welcome to Black Jack 101!\n")
        print_on_canvas("掛け銭: " + str(bet_money), text_position_31)
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

        draw_card(player,dealer)
        print_on_canvas("Your total is " + str(player.hand()), text_position_11)
        print_on_canvas("掛け銭: " + str(bet_money), text_position_31)
        print_on_canvas("Account: " + str(account), text_position_32)

        while player.hand() < 21 and game_strategy(player,dealer):
            card = table.pop()
            player.append(card)

            draw_card(player,dealer)
            print ("You are dealt " + str(card))
            print_on_canvas("Your total is " + str(player.hand()), text_position_11)
            print_on_canvas("掛け銭: " + str(bet_money), text_position_31)
            print_on_canvas("Account: " + str(account), text_position_32)
    
        if player.hand() > 21:
            dealer.cards[0].state = True
            draw_card(player,dealer)
            winning_point = "lose"
            print_on_canvas("You went over 21!",text_position_11)
            print_on_canvas("You lost!",text_position_12)
            print_on_canvas("掛け銭: " + str(bet_money), text_position_31)
            print_on_canvas("Account: " + str(account), text_position_32)

        else:
            print ("\nThe dealer's hidden card was " + str(dealer.cards[0]))
            while dealer.hand() < 17:
                card = table.pop()
                dealer.append(card)
                print ("Dealer is dealt " + str(card))

            dealer.cards[0].state = True
            draw_card(player,dealer)
            print_on_canvas("The dealer's total is " + str(dealer.hand()), text_position_21)
            print_on_canvas("掛け銭: " + str(bet_money), text_position_31)
            print_on_canvas("Account: " + str(account), text_position_32)

            print_on_canvas("Your total is " + str(player.hand()),text_position_11)
            print_on_canvas("The dealer's total is " +  str(dealer.hand()),text_position_21)

            if dealer.hand() > 21:
                winning_point = "win"
                print_on_canvas("The dealer went over 21!" ,text_position_22)
                print_on_canvas("You win!", text_position_12)
            else:
                if player.hand() > dealer.hand():
                    winning_point = "win"
                    print_on_canvas("You win!",text_position_12)
                elif player.hand() < dealer.hand():
                    winning_point = "lose"
                    print_on_canvas("You lost!",text_position_12)
                else :
                    winning_point = "draw"
                    print_on_canvas("You have a tie!",text_position_12)

        account = Banking(winning_point,bet_money,account)
        record.append([winning_point,bet_money,account,player.hand_but(1),dealer.cards[1].value()])   
        if not game_regulator():
            break
        if game_switch == 0 and (not ask_yesno("\nPlay another round? (y/n) ")):
            black_board.close()
            break
        if now_game == Turning_point:
            information = sub_recording(record) 
              
#######################################################
###################### Action ###########################
#######################################################

for i in range(sampling_number):
    main_game()
    recording(record)
    initialize()



