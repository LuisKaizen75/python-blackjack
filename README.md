# Blackjack Terminal Game

Welcome to the Python Casino! This is a simple yet robust Blackjack game implemented in Python that you can play in your terminal.

## Overview

This project demonstrates that even seemingly simple applications can have complex and valuable implementations in a production environment. It features solid testing and an automated workflow for linting and testing using GitHub Actions.

## How to Play

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Run the game using the following command:
    ```sh
    python app.py
    ```
4. Follow the on-screen instructions to play the game.

## Game Rules

- The game is played with 6 decks of cards.
- The goal is to get as close to 21 without going over.
- Face cards (J, Q, K) are worth 10 points, Aces can be worth 1 or 11 points, and all other cards are worth their face value.
- You can buy all the chips that you need.
- Place your bet and receive your cards.
- You can choose to "Hit" to receive another card or "Stay" to keep your current hand.
- The croupier will reveal their cards and play to get at least 17 points.
- The winner is determined based on the hand values.

## Features

- Random card dealing
- Chip management
- Betting system
- Croupier's turn logic
- Replay option

## Code Structure

- `app.py`: The main script to run the game.
- `blackjack.py`: Contains all the game logic and functions.

## Functions

- `pick_card(deck)`: Picks a random card from the deck.
- `deal_player(player_cards, deck)`: Deals a card to the player.
- `deal_croupier(croupier_cards, deck)`: Deals a card to the croupier.
- `hand_value(hand, announce=True)`: Calculates the value of a hand.
- `find_best_hand(cards)`: Finds the best hand value under 21.
- `fresh_deck(decks=6)`: Creates a fresh deck of cards.
- `buy_chips(player_chips, min_bet)`: Allows the player to buy chips.
- `place_bet(min_bet, max_bet)`: Allows the player to place a bet.
- `check_blackjack(player_cards, croupier_cards, player_chips, player_bet)`: Checks for BlackJack.
- `player_turn(player_cards, deck, player_bet, player_chips)`: Handles the player's turn.
- `croupier_turn(croupier_cards, deck)`: Handles the croupier's turn.
- `winner(player_cards, croupier_cards, player_bet, player_chips)`: Determines the winner.
- `play_again()`: Asks the player if they want to play again.

## Technology Used

This project was made using only base Python, without any external libraries. The `random` module from the Python standard library is used for dealing cards.

## Testing and Automation

- **Linting**: The code is linted using `flake8` to ensure code quality and consistency.
- **Testing**: Comprehensive tests are written using `pytest` to ensure the correctness of the game logic.
- **Code Coverage**: Code coverage is measured using `pytest-cov` and `coverage`.
- **Continuous Integration**: GitHub Actions is used to automate the linting and testing process on every push and pull request to the main branch.

## License

This project is licensed under the MIT License.

## Author

Luis Carlos Garzón.

Feel free to contribute to this project by submitting issues or pull requests.