#from time import sleep
#from cs1media import * 
from cs1graphics import *
import random
import csv
import time 
pause_time = 0


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
text_position_11 은 현재 플레이어의 총점을 알려준다. 
text_position_12 은 현재 플레이어의 승패여부를 알려준다. 
text_position_21 은 딜러의 총점을 알려준다. 
text_position_22 은 딜러가 Bursted 되었는지 알려준다. 
text_position_31 and 32 은 전광판에 플레이어의 잔액과 판 돈이 어떻게 바뀌는지 표시한다. 

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

"""
1. record는 승패여부(=winning_point), 판 돈(=bet_money), 잔고(=account),
(=player.hand_but(1)), 처음 공개된 딜러의 카드의 숫자(=dealer.cards[1].get_value())를 담는 리스트다.  
2. information은 
"""
record = []
information = []
now_game = 1
Game_try = 30
Turning_point = 10
sampling_number = 1
now_sampling = 0


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
    return maxkey

#######################################################
################## Class : Card ############################
#######################################################

# 카드 한 장에 관한 Class다. 
class Card(object):

    # 다이아와 하트는 빨간색, 스페이드와 클로버는 검은색 카드다. 
    def __init__(self,face,suit): 
        self.face = face
        self.suit = suit
        self.value = 0
        if self.suit == 'Diamonds' or self.suit == 'Hearts' :    
            self.color = "red"
        else :
            self.color = "black"
        self.state = True 

    # A와 An 문법을 체크하는 함수다. 
    def __str__(self):
        article = "a"
        if self.face == "Ace":
            article = "an "
        elif self.face == "Jack" or "Queen" or "King":
            article = "a "
        else : 
            article = ""

        return article + str(self.face) + "  of  " + self.suit

    # get_value는 Card 한 장 고유의 점수를 처음 계산하거나 덮어쓸 때 쓰는 내장 함수다.
    # Exception은 고유 점수가 11인 Ace가 부득이하게 고유 점수를 1로 계산해야하는 상황을 말한다.
    # Ace가 한 번 1로 계산되면 다시 11이 될 수 없다.  
    def get_value(self, exception=False): 
        try :
            self.value = int(self.face)
            return self.value
        except : 
            if self.face == "Ace" :
                if exception == True or self.value == 1:
                    self.value = 1
                else :
                    self.value = 11
            else :
                self.value = 10
            return self.value

#######################################################
#################### Class : Deck ##########################
#######################################################


class deck(object):

    # self.cards는 deck의 모든 Card Class를 element로 하는 리스트다.
    # self.total은 deck의 계산이 중복되는 것을 막기 위해 쓰이는 value sum 값이다.  
    def __init__(self):
        self.cards = []
        self.total = 0  

    def __len__(self):
        return len(self.cards)

    def clear(self):
        self.cards = []

    # Suit는 [클로버,다이아,하트,스페이드] 모양을 의미한다.
    # Face는 [Ace : 10, J, Q, K ]까지 숫자 또는 그에 준하는 값을 의미한다.
    # table.add_pile() 은 테이블에 카드 한 장을 꺼내는 동작을 의미한다.
    # deck.cards 는 Card Class (카드 한 장)를 원소로 하는 리스트다. 
    def add_pile(self,number=1):
        cards = []
        for i in range(number):
            for suit in suit_names:
                for face in face_names:
                    cards.append(Card(face, suit))
        random.shuffle(cards)
        self.cards = cards

    # deck.hand()는 덱에 들어있는 패들의 점수합을 구하는 내장 함수다.
    # ace_deck은 Ace 카드 들어가는 가상의 덱으로, Ace를 1 또는 11로 계산할지 정하도록 만든다.
    ## ace_deck = [] 는 self.cards 라는 이름의 덱에 Ace의 index를 원소로 하는 리스트다.
    # exception_deck = []는 Ace의 index 중 1로 계산하기로 정한 원소를 따로 모아 놓은 리스트다. 
    # self.cards[i].value의 합을 모두 구하면 self.total에 그 값을 기록한다.
    # Ace가 한 번 value 값이 1이 되었다면 더 이상 ace_deck에 들어가지 않는다. 
    def hand(self, Game_Strategy22 = False):
        self.total = 0 
        ace_deck = []
        exception_deck = []
        for i in range(len(self)):
            self.total += self.cards[i].get_value()
            if self.cards[i].face == "Ace" and self.cards[i].value == 11:
                ace_deck.append(i)
        
        # ace_deck에 Ace가 남아있으면 일단 실행된다.
        # Ace가 있지만 블랙잭이거나 21보다 합이 적으면 11을 굳이 1로 만들 필요가 없다.
        # Game_Strategy22는 손 패가 12~15가 나온 경우 Ace를 1로 놓고 계산한다. 
        while ace_deck:
            
            # Ace가 있는데 손 패가 21을 초과하는 경우 마지막 Ace를 일단 1로 계산한다.
            # Ace가 2장 이상 있을 때 21을 초과하는 경우 한 장 더 1로 계산한다.
            # exception에 포함된 index는 ace_deck에 그 index가 들어있지 않다.
            if self.total > 21 :
                self.total = 0
                exception_deck.append(ace_deck.pop())
                for number in exception_deck:
                    self.cards[number].get_value(exception=True)
                for i in range(len(self)):
                    self.total += self.cards[i].value           
                if self.total <= 21:
                    break
                
            # Game_Strategy22 값이 True일 때 발동한다.
            # 아직 11로 계산되는 Ace가 2장임에도 값이 11에서 16 사이가 나올 수 없다.
            ## len(ace_deck) = 1이다. 
            elif Game_Strategy22 and 11 < self.total < 16:
                self.cards[ace_deck.pop()].get_value(exception=True)
                self.total = 0
                self.total += self.cards[i].value

            # Game_Startegy22를 쓸 것도 아니고, 21을 넘는 것도 아니면 추가적인 계산을 하지 않는다. 
            else :
                break
            
        return self.total
    
    def append(self,card):
        return self.cards.append(card)

    # 
    def pop(self):
        return self.cards.pop()

    # deck.hand_but(number)은 플레이어나 딜러의 덱의 앞에서부터 number개 카드의 value의 합이다.   
    def hand_but(self,number):
        new_deck = deck()
        new_deck.cards = self.cards
        new_value = 0 
        for i in range(number):
            new_value += new_deck.cards[i].value
        return new_value

#######################################################
################# Class : Card Image ########################
#######################################################

def time_out():
    time.sleep(pause_time)

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
##################### Strategy ###########################
#######################################################

game_switch = 3
betting_switch = 1

# 키 조작을 위해 남겨둔 함수다. 
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
        return game_strategy_21(player,dealer)
    elif game_switch == 3:
        return game_strategy_22(player,dealer)

def betting_strategy(record):
    global betting_switch
    if record == [] or betting_switch == 0:
        return minimum_bet 
    elif betting_switch ==1 :
        return betting_strategy_1(record)
    elif betting_switch ==2 :
        return betting_strategy_2(record)

# 가장 기본이 되는 게임 전략이다. switch가 True이면, 용감해진다. 12~16의 수가 나와도 Hit를 하게 된다. 
# 딜러의 오픈된 카드가 2~6 사이면 10을 받아도 한 장 더 받기 때문에, 플레이어는 굳이 Hit할 마음이 없어진다.  
## 다만, 플레이어가 11보다 작은 패가 나왔다면 일단 받고 보는 것이 상책일 것이다. 
def game_strategy_1(player,dealer):
    switch = True 
    if 1 < dealer.cards[1].get_value() < 7:
        switch = False
    if player.hand() < 12: 
        return True 
    elif 11 < player.hand() < 17 and switch :
        return True  
    else:
        return False  

# Inverse Gambler's Fallacy가 적용된다. 
def game_strategy_21(player,dealer):
    global now_game
    global information

    # 처음에는 머릿속을 비우고 일반적인 전략으로 게임을 진행한다. 
    if now_game <= Turning_point: 
        return game_strategy_1(player,dealer)

    # 많은 게임을 하면 근거없는 규칙성(= Inverse Gambler's Fallacy)에 눈을 뜨게 된다. 
    # 카드가 좋지 않은 조합이라고 생각되면 기존 전략과 대비되는 전략을 쓴다.
    """
    예를 들어 Player_worst = 12 이면, 딜러 패에 상관없이 플레이어의 패가 12일 때 자주 패한다.  
    game_strategy_1에서 플레이어의 손 패가 12고 딜러 패가 5가 나왔다면, 상대방의 burst를 기대해야하지만, 
    이 경우 burst를 기대하지 않고 Hit하여 더 나은 패를 손에 쥐고자 할 것이다. 
    """
    Player_worst = information[0]
    Dealer_Lucky = information[1]   
    
    # switch1 = 0은 플레이어의 손 패가 1~11의 약한 수가 나왔을 때, 
    # switch1 = 1은 플레이어의 손 패가 12~16의 애매한 수가 나왔을 때.
    # switch1 = 2는 플레이어의 손 패가 17이상의 믿음직한 수가 나왔을 때를 말한다. 
    switch1 = 0 
    if 11 < player.hand() < 17: 
        switch1 = 1
    elif player.hand() > 16:
        switch1 = 2

    # 플레이어는 우연에 지나지 않은 사건에 전략을 세우고 간섭하여 긍정적인 결과를 만들어내려고 합니다. 
    # switch2가 True이면 용감해져서 Hit를 한다. switch2가 False라면 상대방의 burst를 기대하며 신중해진다. 
    # switch3가 True이면 역발상을 시작한다. 플레이어 Hit -> Stay, Stay -> Hit 로 바꾼다. 
    ## Player_worst = 13 이면 손 패가 12, 13일 때 딜러가 2~6이 나왔더라도 Stay 하지 않고 Hit한다.
    ## Dealer_Lucky = 4 이면 딜러가 4 이하에서 이길 확률이 높아, 딜러가 2나 3이 나온다면 burst를 기대할 수 없다.
    ## 또, 플레이어에게 17이 나왔을 때 마침 Dealer_Lucky라면, 불안해서 Stay 할 카드를 Hit하게 된다.  
    switch2 = True  
    switch3 = False 
    if 1< dealer.cards[1].value < 7:
        switch2 = False  
    if player.hand() <= Player_worst :
        switch3 = True    
    if dealer.cards[1].value <= Dealer_Lucky:
        swtich3 = True 

    """
    Answer는 return할 값으로, True는 Hit을, False는 Stay를 의미한다. 
    """
    Answer = True 
    # switch1과 switch2는 Startegy1와 관계가 같다.  
    # 그러나 switch3은 일정한 경우에 True와 False를 뒤집는다.  
    if not switch1:
        Answer = True 
    elif switch1 == 1 and switch2:
        Answer = True 
    elif switch1 == 1 and not switch2:
        Answer = False 
        if switch3:
            Answer = not Answer
    elif switch1 ==2:
        Answer = False 
        if player.hand() == 17 and switch3:
            Answer = not Answer
    
    return Answer

#이번 전략은 게임 플레이어가 완전한 미치광이 전략을 구사하는 경우다. 
#카드가 랜덤하게 드로우되지 않고, 계산 이상으로 확률의 영향을 크게 받는다고 생각한다. (Gambler's Fallacy, expansion)
#플레이어는 6이하의 카드가 나오면 손 패가 12~16이라고 해도 무조건 한 장 더 받는다. 
#플레이어는 자신의 두 번째 카드 값이 10이고 합이 12이상이면 무조건 Stay를 선언한다.   
#플레이어는 상대방의 오픈된 카드가 10이면 자신은 단 한 장도 Hit하지 않는다. 
# Game_Strategy22는 손 패가 12~15가 나온 경우 Ace를 1로 놓고 계산한다.
def game_strategy_22(player,dealer):
    global now_game
    
    #플레이어는 신내림을 받는다. Answer가 True일 때 Hit, False일 때 Stay다. 
    #일단 game_strategy_1에 따라 기정 결론을 내리고 다시 생각을 한다. 
    Answer = game_strategy_1(player,dealer)
    value_sum = player.hand(Game_Strategy22=True) 
    if len(player.cards)>1 and player.cards[1].value == 10 and value_sum >11:
        Answer = False
    elif player.cards[-1].value < 6 and value_sum < 17:
        Answer = True
    elif dealer.cards[1].value == 10 and player.cards[-1].value < 6:
        Answer = False 
    
    return Answer
        
# 마틴게일 베팅법. 지면 판돈을 무조건 2배로 올린다. 이기면 다시 최소 배팅으로 돌아간다. 
# 다만, 강원랜드는 30만 원으로 판 돈의 한도가 정해져 있으므로, 그 이상을 넘지 못한다. 
# 최대 베팅으로 승리를 거머쥐었지만, 그 최대 베팅액보다 더 많은 돈을 잃은 상태라면, 다시 최대 베팅을 간다.  
def betting_strategy_1(record):
    (winning_point,bet_money,account,player_deck,dealer_deck)=tuple(record[-1])
    if winning_point == "lose":
        bet_money *= 2
        if bet_money > maximum_bet:
            bet_money = maximum_bet
    elif winning_point == "win" :
        if bet_money == maximum_bet and account <= -maximum_bet :
            bet_money = maximum_bet
        else :
            bet_money = minimum_bet             
    return bet_money

# 일반적으로 패배하면 마틴게일 베팅법에 의해 판돈을 2배로 올린다. 
# 그러나 두 번 연속 승리를 거머쥔다면 운수 좋은 날이라고 판단해 갑자기 판돈을 3배로 올린다. 
## 이 경우, 판돈을 5배 올렸는데 패배했다면 기가 죽어 다시 최소 베팅으로 돌아간다. 
## 역시 판돈이 최대 베팅액에 도달하면 30만 원으로 유지된다. 
def betting_strategy_2(record):
    (winning_point,bet_money,account,player_deck,dealer_deck)=tuple(record[-1])
    if winning_point == "lose":
        bet_money *= 2
        if len(record) >2 :            
            check_excited = (record[-2][1] == record[-3][1]*3)
            if check_excited:
                bet_money = minimum_bet
        if bet_money > maximum_bet:
            bet_money = maximum_bet    
    elif  winning_point == "win":
        bet_money = minimum_bet
        if len(record) >1 and record[-2][0] == "win":
            bet_money = record[-2][1]*3
        if bet_money >= maximum_bet and account < maximum_bet:
            bet_money = maximum_bet    
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
    # 플레이어 1인에 대한 기록이 담기는 파일 
    file_name = "strategy_" + str(now_sampling) +".csv" 
    with open(file_name, "wt", encoding = "utf-8" , newline ="") as csv_record:
        writer = csv.writer(csv_record)
        writer.writerow(["W/D/L","Betting","Account","Player_info","Dealer_info"])
        for line in record:
            writer.writerow(line)
            if line[0] == "win" :
                total_winning += 1
            elif line[0] == "lose":
                if 11< line[3] :
                    player_info.append(line[3])
                if line[4]< 7 :
                    dealer_info.append(line[4])
        writer.writerow(["Rate","Player_worst","Dealer_Lucky"])
        Rate = round(total_winning / len(record),3)
        Player_worst = most_frequent(player_info)
        Dealer_Lucky = most_frequent(dealer_info)
        writer.writerow([Rate,Player_worst,Dealer_Lucky])
    csv_record.close

# 과거 게임을 반영하도록 기록하는 함수다.
# 플레이어는 최초에  자신의 오픈된 카드가 얼마였을 때 가장 많이 패배했는지 기억한다. (=Player_worst)
# 플레이어는 딜러의 최초 오픈된 카드가 얼마였을 때 가장 많이 승리했는지도 기억한다. (=Dealer_Lucky)
# data[3] 은 플레이어의 최초 오픈된 카드의 값이고, data[4]는 딜러의 최초 오픈된 카드의 값이다.
## 11< data[3] 일 때 10, J, Q, K를 받거나, 17이 넘을 때까지 계속 받다가 bursted 되기 때문에 트라우마로 남고,
## data[4] < 7 일 때 상대방이 bursted 될 확률이 높음에도 자신보다 훌륭한 수가 완성되면 트라우마로 남는다. 
def sub_recording(record):
    player_info = []
    dealer_info = []
    for data in record:
        if data[0] == "lose":
            if 11< data[3] :
                player_info.append(data[3])
            elif data[4] < 7 :
                dealer_info.append(data[4]) 

    Player_worst, Dealer_Lucky = most_frequent(player_info), most_frequent(dealer_info)        
    return (Player_worst,Dealer_Lucky) 

#######################################################
################## Main game operator ######################
#######################################################

def main_game():

    global bet_money, account, information 
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
        time_out()

        # 패가 21을 넘어가지 않는 선에서, 게임 전략에 따라 Hit을 한다. 
        # 카드를 한장 뽑고, 플레이어에게 넘긴다. (= 플레이어의 덱에 추가된다.)
        while player.hand() < 21 and game_strategy(player,dealer):
            card = table.pop()
            player.append(card)
            print ("You are dealt " + str(card))            
            
            draw_card(player,dealer)
            print_on_canvas("Your total is " + str(player.hand()), text_position_11)
            print_on_canvas("掛け銭: " + str(bet_money), text_position_31)
            print_on_canvas("Account: " + str(account), text_position_32)            
            time_out()

        # 플레이어 손 패가 21이 넘을 때, 딜러의 감춰진 카드를 뒤집는다.
        # winning_point에 플레이어가 패배했음을 기록한다. 
        if player.hand() > 21:
            dealer.cards[0].state = True
            winning_point = "lose"
            
            draw_card(player,dealer)
            print_on_canvas("You went over 21!",text_position_11)
            print_on_canvas("You lost!",text_position_12)
            print_on_canvas("掛け銭: " + str(bet_money), text_position_31)
            print_on_canvas("Account: " + str(account), text_position_32)            
            time_out()

        # 플레이어 손 패가 21이 넘지 않고 더 이상 Hit 하지 않을 때.
        # 딜러의 패를 공개한다. 
        else:

            # 딜러는 본인의 손 패가 16을 넘을 때까지 카드를 뽑는다. 
            while dealer.hand() < 17:
                card = table.pop()
                dealer.append(card)
                print ("Dealer is dealt " + str(card))
                
            print ("\nThe dealer's hidden card was " + str(dealer.cards[0]))                
            dealer.cards[0].state = True
            
            draw_card(player,dealer)
            print_on_canvas("The dealer's total is " + str(dealer.hand()), text_position_21)
            print_on_canvas("掛け銭: " + str(bet_money), text_position_31)
            print_on_canvas("Account: " + str(account), text_position_32)
            print_on_canvas("Your total is " + str(player.hand()),text_position_11)
            print_on_canvas("The dealer's total is " +  str(dealer.hand()),text_position_21)
            time_out()

            # 딜러가 Bursted 되었을 때.
            if dealer.hand() > 21:
                winning_point = "win"
                print_on_canvas("The dealer went over 21!" ,text_position_22)
                print_on_canvas("You win!", text_position_12)
                time_out()

            # 딜러와 플레이어의 패를 비교한다. 
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
                time_out()
                
        # 계좌는 승패여부를 보고 판돈을 잔고에서 뺄지 더할지 판단한다. 
        # 게임기록은 승점, 판돈, 잔액, 플레이어 최악의 패, 딜러 최고의 패를 기록한다. 
        account = Banking(winning_point,bet_money,account)
        record.append([winning_point,bet_money,account,player.hand_but(2),dealer.cards[1].value])   
        if not game_regulator():
            break
        # 수동모드 일 때는 리겜할지 물어본다. 
        if game_switch == 0 and (not ask_yesno("\nPlay another round? (y/n) ")):
            black_board.close()
            break
        # Turning point는 플레이어가 Inverse Gambler's Fallacy에 빠져 전략을 수정하기 전까지 게임 판 수다. 
        if now_game == Turning_point:
            information = sub_recording(record)
                      
#######################################################
###################### Action ###########################
########################################################

for i in range(now_sampling,sampling_number):
    main_game()
    recording(record)
    initialize()
black_board.close()

#######################################################
################# Data Analysis #######################
########################################################

new_data = []
note_name ="All_in_one.csv"

with open(note_name,'wt',encoding ='utf-8', newline ="") as statistic:
    writer = csv.writer(statistic)
    for i in range(sampling_number):
        file_name = "strategy_" + str(i) + ".csv"
        line_number = 0
        account = 0
        rate = 0 
        with open(file_name,'rt', encoding = 'utf-8', newline = "") as experiment:
            reader = csv.reader(experiment)
            for row in reader:
                line_number += 1 
                if not (line_number == Game_try +1 or line_number == Game_try +3) :
                    continue
                elif line_number == Game_try +1:
                    account = row[2]
                    continue
                else :
                    rate = row[0]
        experiment.close()
        new_data = [account,rate]
        writer.writerow(new_data)
statistic.close()




