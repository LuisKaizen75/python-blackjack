import pyfiglet

from blackjack import (
    deal_player, deal_croupier, hand_value, fresh_deck, buy_chips, place_bet,
    check_blackjack, player_turn, croupier_turn, winner, play_again
)

# Welcome to BlackJack terminal game
welcome_message = pyfiglet.figlet_format("Welcome to the Python Casino")
print(welcome_message)
print("¡Good luck!\n")


# Starting game
player_chips = 0
min_bet = 5
max_bet = 100
decks = 6
deck = fresh_deck(decks)
game_on = 1
player_bet = None


while game_on == 1:

    # Buying chips.
    print(f"\nYour chips are: ${player_chips}")
    player_chips = buy_chips(player_chips, min_bet)
    player_bet = place_bet(min_bet, max_bet, player_chips)

    # Game
    # Dealing
    if (len(deck)/(52*decks)) < 0.15:
        deck = fresh_deck()

    # New hand
    player_cards = []
    croupier_cards = []

    # First Hand
    deal_player(player_cards, deck)
    deal_croupier(croupier_cards, deck)
    deal_player(player_cards, deck)
    deal_croupier(croupier_cards, deck)

    # Check BlackJack
    player_chips, blackjack = check_blackjack(
        player_cards, croupier_cards,
        player_chips, player_bet)

    if blackjack:
        game_on = play_again()
        continue

    # Hit
    print("\n--- Your turn ---")
    player_chips, player_bust = player_turn(
                                player_cards, deck,
                                player_bet, player_chips)

    if player_bust:
        game_on = play_again()
        continue

    print("\n--- Croupier is playing ---")

    print("\n--- Croupier reveals his card ---")
    croupier_cards = croupier_turn(croupier_cards, deck)

    if min(hand_value(croupier_cards, False)) > 21:
        print(f"Croupier's hand is more than 21. You won ${player_bet*2}")
        player_chips = player_chips + player_bet*2
        game_on = play_again()
        continue

    # Winner
    player_chips = winner(
        player_cards, croupier_cards,
        player_bet, player_chips)

    game_on = play_again()

print(f"Good Bye, you got ${player_chips}")
