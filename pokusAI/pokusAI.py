import random
import os
import time
import keyboard
import msvcrt
# Function to calculate the value of a hand

def hand_value(hand):
    total = sum(hand)
    number_of_aces = hand.count(11)
    while total > 21 and number_of_aces:
        total = total - 10
        number_of_aces = number_of_aces -1
    return total

#best move based on basic strategy (wiki)
def basic_strategy(base_player_hand, dealer_card):
    player_score = hand_value(base_player_hand)
    
    if player_score >= 17:
        return 's'  # stand/stay
    elif player_score <= 11:
        return 'h'  # hit/play
    else:
        return 's' if dealer_card in [2, 3, 4, 5, 6] else 'h'
    
#player who counts cards and uses max       safe
def count_cards_minimax(deck):
    # strategy/heuristics
    count = sum(1 if card in [2, 3, 4, 5, 6] else -1 if card in [10, 11] else 0 for card in deck)
    count += count #safe zone
    return 'h' if count < 0 else 's'    

#player who counts cards and uses max       scared risk
def risk_count_cards_minimax(deck,risk_deck_counter_player_hand):
    #print(risk_deck_counter_player_hand)
    risk_sum = hand_value(risk_deck_counter_player_hand)
    risk_limit = 21-risk_sum
    good_list = [i for i in range(2, risk_limit+1)]     #bez es
    if hand_value(risk_deck_counter_player_hand)<21:
        if len(good_list)<10:
            good_list.append(11)        #s esy
    if len(good_list)>1:
        var_list = [good_list[-1]]
    else:
        var_list = [-1]
    # strategy/heuristics
    #count = sum(-1 if card in good_list else +1 if card in var_list else +1 for card in deck)      #bezpecnostni prvek
    count = sum(-1 if card in good_list else +1 for card in deck)       #bez bezpecnosti
    count += 1  #scared part
    #print(count)
    return 'h' if count < 0 else 's'

"""#######################################################################################################"""
#########################################################################################################
"""#######################################################################################################"""

#player who knows next cards == cheats
def memory_max(deck,player_hand,is_there_casino_player,dealer_hand,beat_hands):    
    my_sum = hand_value(player_hand)
    deal_sum = hand_value(dealer_hand)
    if is_there_casino_player == True:
        if deal_sum<17:                                             #deal bude muset brat
            #jak dostat casino co nejblize 21
            if hand_value(player_hand)<21:                                       #paklize si vbc muze casino hrac brat
                result=can_casino_win(deck,player_hand,dealer_hand,beat_hands)

                if result[0]==True:                                           #casino can win
                    return result[1]        #vrati pocet kolik karet bych si mel vzit aby casino vyhralo
                else:
                    return 'h' if my_sum + deck[-1] <= 21 else 's'      # #abych nevypadal podezdrele tak kdyz kasino nemuze nic delat tak se snazim vyhrat
            
            else:
                return 's'
        else:
            return 'h' if my_sum + deck[-1] <= 21 else 's'      # #abych nevypadal podezdrele tak kdyz kasino nemuze nic delat tak se snazim vyhrat

    else:
        return 'h' if my_sum + deck[-1] <= 21 else 's'
    
def can_casino_win(deck,player_hand,dealer_hand,beat_hands):   #kolikrat si musim vzit aby byl co nejbliz a jaka je ta hodnota kdyz je nejbliz
    how_many = how_many_can_i_take(deck,player_hand)
    poss=[]
    pom_deck = deck.copy()
    #dealer_hand_var = dealer_hand.copy()

    #predpoklad ze jsem schopen vzit alespon jednu kartu je splnen vzdy kdyz se dostanu sem
    for element in range(0,how_many+1):   #budu potrebovat vsechny moznosti
        pom_pom_deck = pom_deck.copy()
        dealer_hand_var = dealer_hand.copy()
        poss_max = 0
        while (hand_value(dealer_hand_var+[(pom_pom_deck[-1])]))<=21:                          #bude pod 21 pokracuj
            if hand_value(dealer_hand_var)<17:
                dealer_hand_var.append(pom_pom_deck.pop())
                poss_max=hand_value(dealer_hand_var)                     #mam hodnotu nejbliz 21
            else:
                break
        pom_deck.pop()
        poss.append(poss_max)

    indx_max_val = poss.index(max(poss))
    max_val = max(poss)

    num_of_beat = 0
    for i in beat_hands:                                                       #kolik s tou hodnotou kasino porazi hracu?
        if hand_value(i)<=21:
            if max_val>hand_value(i):
                num_of_beat += 1
        #else podle me nema smysl psat

    if num_of_beat>1:
        return [True, indx_max_val]
    else:
        return  [False, None]
    
def how_many_can_i_take(deck,player_hand):
    pom_deck = deck.copy()
    player_hand_var = player_hand.copy()
    i=0
    while hand_value(player_hand_var)<21:
        player_hand_var.append(pom_deck.pop())
        i += 1
    return i
"""#######################################################################################################"""
#########################################################################################################
"""#######################################################################################################"""

def player_turn(deck, player_hand):
    while hand_value(player_hand) < 21:
        print("Player's (yours) Hand:", player_hand)
        keyboard.unhook_all()
        while msvcrt.kbhit():
            msvcrt.getch()
        action = input("Do you want to Hit or Stand? (h/s): ").lower()
        keyboard.hook(lambda e: False)
        if action == 'h':
            player_hand.append(deck.pop())
        elif action == 's':
            break
        else:
            print("Invalid input. Please enter 'h' or 's'.")
    return player_hand

def win_check(player_score, dealer_score):
    if player_score>21:
        return "Lost (over 21)."
    elif dealer_score > 21 or player_score > dealer_score:
        return "Wins!"
    elif player_score == dealer_score:
        return "Draw!"
    else:
        return "Lost (Dealer was closer to 21)."
    
"""def dealer_check(dealer_score):
    if dealer_score>21:
        return "Maybe lost (over 21)."
    else:
        return "Maybe won (if was closer to 21)."   """

# Play
def play_blackjack():
    keyboard.unhook_all()
    while msvcrt.kbhit():
        msvcrt.getch()
    action = input("\nDo you want Casino Player (tries to cheat a bit so casino has got better chance to win if it is possible) to also play? (if yea write: yes): ").lower()
    keyboard.hook(lambda e: False)
    if action == 'yes':
        is_there_casino_player = True
    else:
        is_there_casino_player = False
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
    #print(deck)
    random.shuffle(deck)
    #print(deck)
    table = []
    
    card=deck.pop()
    base_player_hand = [card]
    table.append(card)

    card=deck.pop()
    deck_counter_player_hand = [card]
    table.append(card)

    card=deck.pop()
    risk_deck_counter_player_hand = [card]
    table.append(card)

    card=deck.pop()
    player_hand = [card]
    table.append(card)

    card=deck.pop()
    memory_palace_player_hand = [card]
    table.append(card)

    if is_there_casino_player:
        card=deck.pop()
        casino_player_hand = [card]
        table.append(card)

    card=deck.pop()
    dealer_hand = [card]
    table.append(card)
    ################################################### 
    card=deck.pop()   
    base_player_hand.append(card)
    table.append(card)

    card=deck.pop()
    deck_counter_player_hand.append(card)
    table.append(card)

    card=deck.pop()
    risk_deck_counter_player_hand.append(card)
    table.append(card)

    card=deck.pop()
    player_hand.append(card)
    table.append(card)

    card=deck.pop()
    memory_palace_player_hand.append(card)
    table.append(card)

    if is_there_casino_player:
        card=deck.pop()
        casino_player_hand.append(card)
        table.append(card)

    card=deck.pop()
    dealer_hand.append(card)
    #table.append(card)

    print("\n#####    TABLE   #####\n")

    if is_there_casino_player:
        print("base_player_hand:",base_player_hand,"\ndeck_counter_player_hand:",deck_counter_player_hand,"\nrisk_deck_counter_player_hand:",risk_deck_counter_player_hand,
              "\nplayer_hand:",player_hand,"\nmemory_palace_player_hand:",memory_palace_player_hand,"\ncasino_player_hand:",casino_player_hand,"\ndealer_hand: [",dealer_hand[0],", X]")
    else:
        print("base_player_hand:",base_player_hand,"\ndeck_counter_player_hand:",deck_counter_player_hand,"\nrisk_deck_counter_player_hand:",risk_deck_counter_player_hand,
              "\nplayer_hand:",player_hand,"\nmemory_palace_player_hand:",memory_palace_player_hand,"\ndealer_hand: [",dealer_hand[0],", X]")
    """
    if is_there_casino_player:
        print(base_player_hand,deck_counter_player_hand,risk_deck_counter_player_hand,player_hand,memory_palace_player_hand,casino_player_hand,dealer_hand)
    else:
        print(base_player_hand,deck_counter_player_hand,risk_deck_counter_player_hand,player_hand,memory_palace_player_hand,dealer_hand)"""
    time.sleep(4)
    dealer_card = dealer_hand[0]

    
    print("\n#####    GAME   #####\n")
    
    #base_player turn
    while hand_value(base_player_hand) < 21:
        print("Base Player's Hand:", base_player_hand)
        action = basic_strategy(base_player_hand, dealer_card)
        print("Base Player chooses to: ", "Hit" if action == 'h' else "Stand")
        if action == 'h':
            card = deck.pop()
            base_player_hand.append(card)
            table.append(card)
            if hand_value(base_player_hand) > 21:
                print("Base Player's Hand:", base_player_hand,"Base Player lost.")
                break            
            if hand_value(base_player_hand) == 21:
                print("Base Player's Hand:", base_player_hand)
                break
        elif action == 's':
            break
    print("\nBase Player's final Hand:", base_player_hand ,"Value of the Hand is: ", hand_value(base_player_hand))
    time.sleep(3)
    print("\n")

    #deck_counter turn with some safe space
    while True:
        print("Deck Counter safe Player's Hand:", deck_counter_player_hand)
        if hand_value(deck_counter_player_hand) < 18:
            if hand_value(deck_counter_player_hand) < 12:
                action = 'h'
            else:
                action = count_cards_minimax(table)
        else: 
            action = None
        print("Deck Counter safe Player chooses to: ", "Hit" if action == 'h' else "Stand")
        if action == 'h':
            card = deck.pop()
            deck_counter_player_hand.append(card)
            table.append(card)
            if hand_value(deck_counter_player_hand) > 21:
                print("Deck Counter safe Player's Hand:", deck_counter_player_hand,"Deck Counter safe Player lost.")
                break
        else:
            break
    print("\nDeck Counter safe Player's final Hand:", deck_counter_player_hand,"Value of the Hand is: ", hand_value(deck_counter_player_hand))
    time.sleep(3)
    print("\n")

    #deck_counter turn with scared risk
    while True:
        print("Deck Counter risk Player's Hand:", risk_deck_counter_player_hand)
        scared_deck = deck
        scared_deck.append(dealer_hand[1])
        action = risk_count_cards_minimax(scared_deck,risk_deck_counter_player_hand)
        print("Deck Counter risk Player chooses to: ", "Hit" if action == 'h' else "Stand")
        if action == 'h':
            card = deck.pop()
            risk_deck_counter_player_hand.append(card)
            #print(risk_deck_counter_player_hand)
            if hand_value(risk_deck_counter_player_hand) > 21:
                print("Deck Counter risk Player's Hand:", risk_deck_counter_player_hand,"Deck Counter risk Player lost.")
                break
        else:
            break
    print("\nDeck Counter risk Player's final Hand:", risk_deck_counter_player_hand,"Value of the Hand is: ", hand_value(risk_deck_counter_player_hand))
    time.sleep(3)
    print("\n")

    #true_player
    player_hand = player_turn(deck, player_hand)
    if  hand_value(player_hand)>21:
        print("Player's (your) Hand:", player_hand,"Player (you) lost.")
    print("\nPlayer's (your) final Hand:", player_hand,"Value of the Hand is: ", hand_value(player_hand))
    time.sleep(3)
    print("\n")

    #memory max
    beat_hands = [None]
    while True:
        print("Memory palace Player's Hand:", memory_palace_player_hand)
        #want_casino_player = False
        action = memory_max(deck,memory_palace_player_hand,False,dealer_hand,beat_hands)
        print("Memory palace Player chooses to: ", "Hit" if action == 'h' else "Stand")
        if action == 'h':
            memory_palace_player_hand.append(deck.pop())
            if hand_value(memory_palace_player_hand) > 21:
                print("Memory palace Player lost.")
                break
        else:
            break
    print("\nMemory palace Player's final Hand:", memory_palace_player_hand,"Value of the Hand is: ", hand_value(memory_palace_player_hand))
    time.sleep(3)
    print("\n")

    #casino player
    beat_hands = [base_player_hand, deck_counter_player_hand,risk_deck_counter_player_hand,player_hand,memory_palace_player_hand]
    while is_there_casino_player == True:
        print("Casino Player's Hand:", casino_player_hand)
        action = memory_max(deck,casino_player_hand,is_there_casino_player,dealer_hand, beat_hands)
        if action == 's':
            print("Casino Player chooses to: Stand")
            break
        elif isinstance(action, int):
            print("Casino Player chooses to: Make someone cry")
            num_hits = action
            for _ in range(num_hits):
                casino_player_hand.append(deck.pop())
                if hand_value(casino_player_hand) > 21:
                    print("Casino Player lost.")
                    break
            print("Casino Player's Hand:", casino_player_hand)
            break
        else:            
            print("Casino Player chooses to: Hit")
            casino_player_hand.append(deck.pop())
            if hand_value(casino_player_hand) > 21:
                print("Casino Player lost.")
                break
            print("Casino Player's Hand:", casino_player_hand)
            break
    if  is_there_casino_player == True:
        print("\nCasino Player's final Hand:", casino_player_hand,"Value of the Hand is: ", hand_value(casino_player_hand))
        time.sleep(3)
    
    #Dealer's turn
    while hand_value(dealer_hand) < 17:
        dealer_hand.append(deck.pop())
    print("\nDealer's final Hand:", dealer_hand,"Value of the Hand is: ", hand_value(dealer_hand))
    time.sleep(3)
    
    #winner?
    base_player_score = hand_value(base_player_hand)
    deck_counter_player_score = hand_value(deck_counter_player_hand)
    risk_deck_counter_player_score = hand_value(risk_deck_counter_player_hand)
    player_score = hand_value(player_hand)
    memory_palace_player_score = hand_value(memory_palace_player_hand)
    if  is_there_casino_player == True:
        casino_player_score = hand_value(casino_player_hand)
    dealer_score = hand_value(dealer_hand)
    
    print("\n\nfinal hands and values\n\n")
    print("Base Player's Hand:              ", base_player_hand, " Value of the hand is: ",hand_value(base_player_hand))
    print("Deck Counter safe Player's Hand: ", deck_counter_player_hand, " Value of the hand is: ",hand_value(deck_counter_player_hand))
    print("Deck Counter risk Player's Hand: ", risk_deck_counter_player_hand, " Value of the hand is: ",hand_value(risk_deck_counter_player_hand))
    print("Players (your) Hand:             ", player_hand, " Value of the hand is: ",hand_value(player_hand))
    print("Memory palace Player's Hand:     ", memory_palace_player_hand, " Value of the hand is: ",hand_value(memory_palace_player_hand))
    if  is_there_casino_player == True:
        print("Casino Player's Hand:            ", casino_player_hand, " Value of the hand is: ",hand_value(casino_player_hand))
    print("Dealer's Hand:                   ", dealer_hand, " Value of the hand is: ",hand_value(dealer_hand))

    print("\nfinal results\n")
    print("Base Player:                 ", win_check(base_player_score, dealer_score))
    print("Deck Counter safe Player:    ", win_check(deck_counter_player_score, dealer_score))
    print("Deck Counter risk Player:    ", win_check(risk_deck_counter_player_score, dealer_score))
    print("Player (you):                ", win_check(player_score, dealer_score))
    print("Memory palace Player:        ", win_check(memory_palace_player_score, dealer_score))
    if  is_there_casino_player == True:
        print("Casino Player:               ", win_check(casino_player_score, dealer_score))
    #print("Dealer's Hand:", dealer_check(dealer_score))
    #print(deck)

    if is_there_casino_player == True:
        return [ win_check(base_player_score, dealer_score), win_check(deck_counter_player_score, dealer_score), win_check(risk_deck_counter_player_score, dealer_score),
                win_check(player_score, dealer_score), win_check(memory_palace_player_score, dealer_score), win_check(casino_player_score, dealer_score), 1]
    else:
        return [ win_check(base_player_score, dealer_score), win_check(deck_counter_player_score, dealer_score), win_check(risk_deck_counter_player_score, dealer_score),
                win_check(player_score, dealer_score), win_check(memory_palace_player_score, dealer_score), 0]



# Play the game
keyboard.hook(lambda e: False)
game = 0
os.system('cls')
wanna_play = True
with_cas_play = []
without_cas_play = []
while wanna_play:
    stat = play_blackjack()
    game += 1
    if stat[-1] == 1:
        with_cas_play.append(stat)
    if stat[-1] == 0:
        without_cas_play.append(stat)

    keyboard.unhook_all()
    while msvcrt.kbhit():
        msvcrt.getch()
    print("\nYou finished game number",game)
    wanna_play_var = input("\n\nDo you want to QUIT the game (if yes type yes)?\n\n").lower()
    keyboard.hook(lambda e: False)
    if wanna_play_var == 'yes':
        wanna_play = False


print("\n\ncasplay:",with_cas_play)
print("\n\nNOcasplay:",without_cas_play)
print("\n")
      
base_player_stats1 = [0, 0, 0]
deck_counter_stats1 = [0, 0, 0]
risk_deck_counter_stats1 = [0, 0, 0]
player_stats1 = [0, 0, 0]
memory_palace_stats1 = [0, 0, 0]
casino_player_stats1 = [0, 0, 0]

stat1_list = [base_player_stats1, deck_counter_stats1, risk_deck_counter_stats1, player_stats1, memory_palace_stats1, casino_player_stats1]

base_player_stats2 = [0, 0, 0]
deck_counter_stats2 = [0, 0, 0]
risk_deck_counter_stats2 = [0, 0, 0]
player_stats2 = [0, 0, 0]
memory_palace_stats2 = [0, 0, 0]

stat2_list = [base_player_stats2, deck_counter_stats2, risk_deck_counter_stats2, player_stats2, memory_palace_stats2]

for i in range(len(with_cas_play)):
    #print("i",i)
    for j in range(len(with_cas_play[i])-1):
        #print("j",j)
        if with_cas_play[i][j] == "Wins!":
            stat1_list[j][0] += 1
        elif with_cas_play[i][j] == "Lost (over 21)." or with_cas_play[i][j] == "Lost (Dealer was closer to 21).":
            stat1_list[j][1] += 1
        elif with_cas_play[i][j] == "Draw!":
            stat1_list[j][2] += 1

for m in range(len(without_cas_play)):
    for n in range(len(without_cas_play[m])):
        if without_cas_play[m][n] == "Wins!":
            stat2_list[n][0] += 1
        elif without_cas_play[m][n] == "Lost (over 21)." or without_cas_play[m][n] == "Lost (Dealer was closer to 21).":
            stat2_list[n][1] += 1
        elif without_cas_play[m][n] == "Draw!":
            stat2_list[n][2] += 1

print("\nStats for games with Casino Player\n")
print("Number of games:",len(with_cas_play))
print(stat1_list)
print("Base Player stats (Win/Loss/Draw):                 ", stat1_list[0])
print("Deck Counter safe Player stats (Win/Loss/Draw):    ", stat1_list[1])
print("Deck Counter risk Player stats (Win/Loss/Draw):    ", stat1_list[2])
print("Player (you) stats (Win/Loss/Draw):                ", stat1_list[3])
print("Memory palace Player stats (Win/Loss/Draw):        ", stat1_list[4])
print("Casino Player stats (Win/Loss/Draw):               ", stat1_list[5])

print("\nStats for games without Casino Player\n")
print("Number of games:",len(without_cas_play))
print(stat2_list)
print("Base Player stats (Win/Loss/Draw):                 ", stat2_list[0])
print("Deck Counter safe Player stats (Win/Loss/Draw):    ", stat2_list[1])
print("Deck Counter risk Player stats (Win/Loss/Draw):    ", stat2_list[2])
print("Player (you) stats (Win/Loss/Draw):                ", stat2_list[3])
print("Memory palace Player stats (Win/Loss/Draw):        ", stat2_list[4])

keyboard.unhook_all()
print("\nPress any key to end")
msvcrt.getch()