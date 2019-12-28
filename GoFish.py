from Cards import Card
from Cards import Deck
from Cards import Hand
import random
import os


def printHand():
    os.system('cls')
    for i in range(no_of_players):
        print("Cards of Player " + str(i))
        hand[i].cards.sort(key=lambda x: x.rank, reverse=False)
        print(hand[i])
        print()


def printPlayerHand(h):
    # os.system('cls')
    print("Cards of Player " + str(h))
    hand[h].cards.sort(key=lambda x: x.rank, reverse=False)
    print(hand[h])
    print()


deck = Deck()
deck.shuffle()

no_of_players = int(input("Enter Numbers Of Players : "))
if no_of_players == 2:
    no_of_cards = 7
else:
    no_of_cards = 5

hand = []
win = []
for i in range(no_of_players):
    win.append(0)
if no_of_players < 7:
    for i in range(no_of_players):
        hand.append(Hand())
        deck.move_cards(hand[i], no_of_cards)
    chance = random.randint(0, no_of_players - 1)
    # printHand()
    printPlayerHand(chance)

    while True:
        print(win)
        print("Player " + str(chance) + " has Chance to ask cards ")
        pl = int(input("Enter Player Number : "))
        if chance == pl:
            print("\tERROR : You can't ask to your self! \n")
            continue
        if pl >= no_of_players:
            print("\tERROR : Player Number Exceeded!!\n")
            continue

        rank = int(input("Enter Rank : "))
        if not (hand[chance].check_card(rank)):
            print("\tERROR : You can not ask for card which you don't have with similar rank\n")
            continue

        temp = hand[pl].trasfer_card(hand[chance], rank)
        count = 0
        x = []
        for i in hand[chance].cards:
            if i.rank == rank:
                x.append(i)
                count += 1
        if count == 4:
            for i in x:
                hand[chance].remove_card(i)
            win[chance] += 1

        # printHand()
        printPlayerHand(chance)
        if hand[pl].length() == 0:
            break
        if temp == 1:
            continue
        try:
            temp = deck.pop_card()
            hand[chance].add_card(temp)
            count = 0
            x = []
            for i in hand[chance].cards:
                if i.rank == temp.rank:
                    x.append(i)
                    count += 1
            if count == 4:
                for i in x:
                    hand[chance].remove_card(i)
                win[chance] += 1
            if hand[chance].length() == 0:
                break
            # printHand()
            printPlayerHand(chance)
            os.system('cls')
            print("=============Go Fish=============\n")
            print("Selected From Pile : " + str(temp) + "  (" + str(deck.count_card()) + ")")

            if temp.rank == rank:
                printPlayerHand(chance)
                continue
        except IndexError:
            print("Empty pile\n")
            break
        chance = pl
        printPlayerHand(chance)

    maximum = max(win)
    winner = win.index(maximum)
    del win[winner]
    try:
        flag = win.index(maximum)
        win.insert(winner, maximum)
        print("*********************Draw**************************")
        for i in win:
            if i == maximum:
                print("Player ->  " + str(i))
        print("has same points.")
    except ValueError:
        print("Player ----------->   " + str(winner) + "   <---------- is **********WINNER!**********")


else:
    print(str(no_of_players) + "  players can not play this game.")
    exit()
