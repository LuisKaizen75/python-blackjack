import random
import time


def pick_card(deck):
    card = random.choice(deck)
    del deck[deck.index(card)]
    return card


def deal_player(player_cards, deck):
    time.sleep(1)
    card = pick_card(deck)
    player_cards.append(card)
    print(f"\nYour card is: {card}")
    print(f"Your hand is: {player_cards}")


def deal_croupier(croupier_cards, deck):
    time.sleep(1)
    card = pick_card(deck)
    croupier_cards.append(card)
    if len(croupier_cards) != 2:
        print(f"\nCroupier's card is: {card}")
        print(f"Croupier's hand is: {croupier_cards}")
    else:
        print("\nCroupier took his second card \n")


def hand_value(hand, announce=True):

    hand_value = []
    aces = hand.count("A")

    if aces > 0:
        hand = [i for i in hand if i != "A"]
        aces = [1*aces, (aces-1)+11]
        aces = list(set(aces))
    else:
        aces = [0]

    hand = list(map(lambda x: 10 if x in ["J", "Q", "K"] else x, hand))
    hand = sum(hand)
    hand = [i+hand for i in aces]

    minimum = min(hand)

    for i in hand:
        if i <= 21:
            hand_value.append(i)

    if not hand_value:
        hand_value = [minimum]

    message = "Hand value is: "
    for i in range(0, len(hand_value)):
        message += str(hand_value[i])
        if i < len(hand_value)-1:
            message += " or "
    if announce:
        print(message)
    return hand_value


def find_best_hand(cards):
    cards = hand_value(cards, False)
    cards = [i for i in cards if i <= 21]
    if cards:
        better_hand = max(cards)
        return better_hand
    else:
        return 0


def fresh_deck(decks=6):
    freshDeck = []
    print("Shuffling the deck...")
    number_cards = list(range(2, 11))
    face_cards = ["A", "J", "Q", "K"]
    suit = number_cards + face_cards
    deck = suit + suit + suit + suit
    for i in range(decks):
        freshDeck += deck

    return freshDeck


def ask_chips(player_chips, min_bet):
    if player_chips > min_bet:
        while True:
            try:
                buy_chips = int(input("Would you like to buy chips?:\n1) Yes 0) No "))
                if buy_chips in [0, 1]:
                    break
                else:
                    print("\nThat option is not available.")
            except ValueError:
                print("\nPlease enter a whole number.\n")
    else:
        buy_chips = 1
    return buy_chips


def buy_chips(player_chips, min_bet):
    buy_chips = ask_chips(player_chips, min_bet)
    if buy_chips == 1:
        amount = 0
        while True:
            try:
                amount = int(input("Buy your chips (enter the amount): $"))
                if amount < 0:
                    raise ValueError("Cannot buy a negative amount of chips.")
                player_chips += amount
                print(f"You have {player_chips} chips.")
                break
            except ValueError:
                print("Please enter a positive whole number.")
    return player_chips


def place_bet(min_bet, max_bet, player_chips):
    while True:
        try:
            player_bet = int(input(f"\nPlease make your bet (min:{min_bet} - max:{max_bet}): "))
            if min_bet <= player_bet <= max_bet:
                if player_bet > player_chips:
                    print(f"Sorry, you don't have enough chips. You have {player_chips} chips.")
                else:
                    return player_bet
            else:
                print(f"Please enter a bet within the table limits (min:{min_bet} - max:{max_bet})\n")
        except ValueError:
            print("Please enter a whole number.\n")


def check_blackjack(
        player_cards, croupier_cards, player_chips, player_bet):
    '''Return player chips and boolean representing presence of BlackJack'''

    if (max(hand_value(croupier_cards, False)) == 21) and (max(hand_value(player_cards, False)) != 21):
        print("Croupier has BlackJack")
        print(f"You lose ${player_bet}")
        player_chips = player_chips - player_bet
        return player_chips, True

    elif (max(hand_value(player_cards, False)) == 21) and (max(hand_value(croupier_cards, False)) != 21):
        print("You have a BlacKJack!")
        prize = player_bet * 1.5
        print(f"You won ${prize}")
        player_chips = player_chips + prize
        return player_chips, True

    elif (max(hand_value(croupier_cards, False)) == 21) and (max(hand_value(player_cards, False)) == 21):
        print("It's a push")
        return player_chips, True

    return player_chips, False


def player_turn(player_cards, deck, player_bet, player_chips):

    while True:
        if min(hand_value(player_cards)) > 21:
            print(f"Your hand is more than 21. You lose ${player_bet}")
            player_chips = player_chips - player_bet
            player_bust = True
            break
        try:
            hit = int(input("Hit or stay?\n1) Hit. 0) Stay: "))
            if hit == 0:
                player_bust = False
                break
            elif hit == 1:
                deal_player(player_cards, deck)
            else:
                print("Invalid option.")
        except ValueError:
            print("Wrong command entered, please try again.")

    return player_chips, player_bust


def croupier_turn(croupier_cards, deck):
    while max(hand_value(croupier_cards)) < 17:
        deal_croupier(croupier_cards, deck)

    return croupier_cards


def winner(
        player_cards, croupier_cards,
        player_bet, player_chips):

    player_score = find_best_hand(player_cards)
    croupier_score = find_best_hand(croupier_cards)

    if player_score > croupier_score:
        print(f"\nYou won ${player_bet*2}: {player_score} vs {croupier_score}.")
        player_chips = player_chips + player_bet

    elif player_score == croupier_score:
        print(f"\nIt's a tie: {player_score} vs {croupier_score}")

    else:
        print(f"\nYou lose ${player_bet}: {player_score} vs {croupier_score}.")
        player_chips = player_chips - player_bet

    return player_chips


def play_again():
    while True:
        try:
            game_on = int(input("\nPlay again?:\n1) Yes 0) No "))
            if game_on in [0, 1]:
                return game_on
            else:
                print("Sorry, that option is not available.")
        except ValueError:
            print("Please enter an integer number.\n")
