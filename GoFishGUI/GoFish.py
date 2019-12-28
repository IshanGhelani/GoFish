# from Cards import Card
from Cards import Deck
from Cards import Hand
import random
import os
import pygame

img_suit = ["c", "d", "h", "s"]
img_rank = ["a", "2", "3", "4", "5", "6", "7", "8", "9", "10", "j", "q", "k"]

suit_names = ["Clubs", "Diamonds", "Hearts", "Spades"]
rank_names = [None, "Ace", "2", "3", "4", "5", "6", "7",
              "8", "9", "10", "Jack", "Queen", "King"]
display_width = 800
display_height = 600

white = (255, 255, 255)
black = (0, 0, 0)

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (200, 200, 0)

bright_red = (200, 0, 0)
bright_green = (0, 200, 0)
bright_blue = (0, 0, 200)
bright_yellow = (150, 150, 0)


def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()


def button(msg, x, y, w, h, ic, ac, i, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # print(click)
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action(i)
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    smallText = pygame.font.SysFont("comicsansms", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(textSurf, textRect)


def printPlayerHand(h):
    hand[h].cards.sort(key=lambda x: x.rank, reverse=False)
    inc = 20
    w = 230
    for i in range(len(hand[h].cards)):
        img = str(img_suit[hand[h].cards[i].suit]) + str(img_rank[hand[h].cards[i].rank-1]) + ".png"
        image = pygame.image.load(os.path.join("CardsImage", img))
        screen.blit(image, (w, 130))
        w += inc
    # print(hand[h])
    # print()


def updatepl(i):
    global pl
    global error
    global temp
    temp = None
    pl = i
    if chance == pl:
        error = "ERROR : You can't ask to your self!"
    else:
        error = ""


def updaterank(i):
    global rank
    global error
    global temp
    temp = None
    rank = i + 1
    if not (hand[chance].check_card(rank)):
        error = "ERROR : You can not ask for card which you don't have with similar rank"
    else:
        error = ""


def end():
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
    pygame.quit()
    quit()


def maketransfer(_):
    global chance
    global error
    global temp
    temp = None
    for _ in range(no_of_players):
        for j in hand:
            if j.length() == 0:
                end()
    if chance == pl:
        error = "ERROR : You can't ask to your self!"
        return
    if not (hand[chance].check_card(rank)):
        error = "ERROR : You can not ask for card which you don't have with similar rank"
        return
    temp1 = hand[pl].trasfer_card(hand[chance], rank)
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

    printPlayerHand(chance)
    if hand[pl].length() == 0:
        end()
    if temp1 == 1:
        return
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
            end()
        printPlayerHand(chance)

        error = "===GoFish===="

        img = str(img_suit[temp.suit]) + str(img_rank[temp.rank - 1]) + ".png"
        image = pygame.image.load(os.path.join("CardsImage", img))
        screen.blit(image, (700, 130))

        # print("Selected From Pile : " + str(temp) + "  (" + str(deck.count_card()) + ")")

        if temp.rank == rank:
            printPlayerHand(chance)
            return
    except IndexError:
        error = "empty pile"
        end()
    chance = pl
    printPlayerHand(chance)


# ################## MAIN #################


pygame.init()
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("GoFISHPygameApp")
clock = pygame.time.Clock()
deck = Deck()
deck.shuffle()
smallText = pygame.font.SysFont("comicsansms", 20)
mediumText = pygame.font.SysFont("comicsansms", 30)
largeText = pygame.font.SysFont("comicsansms", 50)
temp = None
# no_of_players = int(input("Enter Numbers Of Players : "))
# if no_of_players == 2:
#     no_of_cards = 7
# else:
#     no_of_cards = 5

no_of_players = 3
no_of_cards = 5
hand = []
win = [0] * no_of_players
error = ""

for i in range(no_of_players):
    hand.append(Hand())
    deck.move_cards(hand[i], no_of_cards)
chance = random.randint(0, no_of_players - 1)
# printHand()

pl = 1
rank = 13

while True:
    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    screen.fill(black)
    printPlayerHand(chance)
    if temp is None:
        img = "back.png"
    else:
        img = str(img_suit[temp.suit]) + str(img_rank[temp.rank - 1]) + ".png"
    image = pygame.image.load(os.path.join("CardsImage", img))
    screen.blit(image, (700, 130))

    msg = "Score : [" + str(win[0]) + ", " + str(win[1]) + ", " + str(win[2]) + "]"
    textSurf, textRect = text_objects(msg, mediumText)
    textRect.center = (600, 50)
    screen.blit(textSurf, textRect)

    msg = "player " + str(chance) + " has chance"
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = (100, 50)
    screen.blit(textSurf, textRect)

    msg = "asking to player " + str(pl)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = (100, 150)
    screen.blit(textSurf, textRect)

    msg = "for rank  " + str(rank_names[rank])
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = (100, 250)
    screen.blit(textSurf, textRect)

    button("CONFIRM", 100, 350, 100, 40, yellow, bright_yellow, 0, maketransfer)

    inc = display_width/no_of_players
    h = int(display_height/8)
    w = 0
    for i in range(no_of_players):
        button("player" + str(i), w, 400, 100, 40, blue, bright_blue, i, updatepl)
        w += inc

    inc = display_width / 7
    h = int(display_height / 8)
    w = 0
    for i in range(7):
        button(rank_names[i+1], w, 470, 100, 40, blue, bright_blue, i, updaterank)
        w += inc

    inc = display_width / 6
    h = int(display_height / 8)
    w = 0
    for i in range(7, 13):
        button(rank_names[i + 1], w, 540, 100, 40, blue, bright_blue, i, updaterank)
        w += inc

    textSurf = smallText.render(error, True, red)
    textRect = textSurf.get_rect()
    textRect.center = (400, 300)
    screen.blit(textSurf, textRect)

    pygame.display.update()
    clock.tick(25)

