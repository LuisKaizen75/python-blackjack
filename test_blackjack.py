import pytest
from unittest.mock import patch, call
from blackjack import (pick_card, fresh_deck, deal_player,
                       deal_croupier, hand_value, find_best_hand,
                       buy_chips, place_bet, check_blackjack, player_turn,
                       croupier_turn, winner, play_again)


def test_fresh_deck():
    cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'A', 'J', 'Q', 'K']

    # Counting that each deck has 52 cards.
    for n in range(1, 7):
        deck = fresh_deck(n)
        assert len(deck) == (n*52)

        # Counting 4 cards of each face value per deck.
        for card in cards:
            assert deck.count(card) == n*4


@pytest.fixture
def deck():
    return fresh_deck(6)


@patch('blackjack.random.choice', return_value='A')
def test_pick_card(mock_choice, deck):
    deck_len = len(deck)
    card = pick_card(deck)
    assert card == 'A'
    assert len(deck) == deck_len-1
    assert deck.count('A') == 23


@patch('blackjack.random.choice', return_value='A')
@patch('builtins.print')
def test_deal_player(mock_print, mock_choice, deck):
    player_cards = []
    deal_player(player_cards, deck)
    assert player_cards == ['A']


@patch('blackjack.random.choice', return_value='A')
@patch('builtins.print')
def test_deal_croupier(mock_choice, deck):
    croupier_cards = []
    deal_croupier(croupier_cards, deck)
    assert croupier_cards == ['A']
    deal_croupier(croupier_cards, deck)
    assert croupier_cards == ['A', 'A']


@patch('builtins.print')
def test_hand_value(mock_print):
    hand = []
    value = hand_value(hand)
    assert value == [0]

    hand = ['A']
    value = hand_value(hand)
    assert value == [1, 11]

    hand = ['A', 'K']
    value = hand_value(hand)
    assert value == [11, 21]

    hand = ['A', 'K', 'Q']
    value = hand_value(hand)
    assert value == [21]

    hand = ['A', 'K', 'Q', 'J']
    value = hand_value(hand)
    assert value == [31]

    hand = ['A', 'A', 3]
    value = hand_value(hand)
    assert value == [5, 15]

    hand = ['A', 'A', 'Q', 'J']
    value = hand_value(hand)
    assert value == [22]

    assert mock_print.mock_calls == [call("Hand value is: 0"),
                                     call("Hand value is: 1 or 11"), call("Hand value is: 11 or 21"),
                                     call("Hand value is: 21"), call("Hand value is: 31"),
                                     call("Hand value is: 5 or 15"), call("Hand value is: 22")]


def test_find_best_hand():
    hand = []
    value = find_best_hand(hand)
    assert value == 0

    hand = ['A']
    value = find_best_hand(hand)
    assert value == 11

    hand = ['A', 'K']
    value = find_best_hand(hand)
    assert value == 21

    hand = ['A', 'K', 'Q']
    value = find_best_hand(hand)
    assert value == 21

    hand = ['A', 'K', 'Q', 'J']
    value = find_best_hand(hand)
    assert value == 0

    hand = ['A', 'A', 3]
    value = find_best_hand(hand)
    assert value == 15

    hand = ['A', 'A', 'Q', 'J']
    value = find_best_hand(hand)
    assert value == 0


@patch('builtins.input', side_effect=['50'])
def test_buy_chips_initial(mock_input):
    player_chips = 0
    min_bet = 10
    player_chips = buy_chips(player_chips, min_bet)
    assert player_chips == 50


@patch('builtins.input', side_effect=['1', '50'])
def test_buy_chips_optional(mock_input):
    player_chips = 40
    min_bet = 10
    player_chips = buy_chips(player_chips, min_bet)
    assert player_chips == 90


@patch('builtins.input', side_effect=[0])
def test_buy_chips_no_purchase(mock_input):
    player_chips = 20
    min_bet = 10
    player_chips = buy_chips(player_chips, min_bet)
    assert player_chips == 20


@patch('builtins.input', side_effect=['-50', '50'])
@patch('builtins.print')
def test_buy_chips_initial_error_negative(mock_print, mock_input):
    player_chips = 0
    min_bet = 10
    player_chips = buy_chips(player_chips, min_bet)
    assert mock_print.mock_calls == [call("Please enter a positive whole number."), call("You have 50 chips.")]


@patch('builtins.input', side_effect=['hi', '50'])
@patch('builtins.print')
def test_buy_chips_initial_error_nan(mock_print, mock_input):
    player_chips = 0
    min_bet = 10
    player_chips = buy_chips(player_chips, min_bet)
    assert mock_print.mock_calls == [call("Please enter a positive whole number."), call("You have 50 chips.")]


@patch('builtins.input', side_effect=['1', '-50', '50'])
@patch('builtins.print')
def test_buy_chips_optional_error_negative(mock_print, mock_input):
    player_chips = 20
    min_bet = 10
    player_chips = buy_chips(player_chips, min_bet)
    assert mock_print.mock_calls == [call("Please enter a positive whole number."), call("You have 70 chips.")]


@patch('builtins.input', side_effect=['1', 'hi', '50'])
@patch('builtins.print')
def test_buy_chips_optional_error_nan(mock_print, mock_input):
    player_chips = 20
    min_bet = 10
    player_chips = buy_chips(player_chips, min_bet)
    assert mock_print.mock_calls == [call("Please enter a positive whole number."), call("You have 70 chips.")]


@patch('builtins.input', side_effect=['100', '0'])
@patch('builtins.print')
def test_buy_chips_optional_error_1(mock_print, mock_input):
    player_chips = 20
    min_bet = 10
    player_chips = buy_chips(player_chips, min_bet)
    assert mock_print.mock_calls == [call("\nThat option is not available.")]


@patch('builtins.input', side_effect=['hi', '0'])
@patch('builtins.print')
def test_buy_chips_optional_error_2(mock_print, mock_input):
    player_chips = 20
    min_bet = 10
    player_chips = buy_chips(player_chips, min_bet)
    assert mock_print.mock_calls == [call("\nPlease enter a whole number.\n")]


@patch('builtins.input', side_effect=['20'])
def test_place_bet(mock_input):
    min_bet = 10
    max_bet = 100
    player_chips = 30
    assert place_bet(min_bet, max_bet, player_chips) == 20


@patch('builtins.input', side_effect=['300', '10'])
@patch('builtins.print')
def test_place_bet_error(mock_print, mock_input):
    min_bet = 10
    max_bet = 100
    player_chips = 30
    place_bet(min_bet, max_bet, player_chips)
    assert mock_print.mock_calls == [call("Please enter a bet within the table limits (min:10 - max:100)\n")]


@patch('builtins.input', side_effect=['40', '10'])
@patch('builtins.print')
def test_place_bet_error2(mock_print, mock_input):
    min_bet = 10
    max_bet = 100
    player_chips = 30
    place_bet(min_bet, max_bet, player_chips)
    assert mock_print.mock_calls == [call("Sorry, you don't have enough chips. You have 30 chips.")]


@patch('builtins.input', side_effect=['hi', '10'])
@patch('builtins.print')
def test_place_bet_nan(mock_print, mock_input):
    min_bet = 10
    max_bet = 100
    player_chips = 30
    place_bet(min_bet, max_bet, player_chips)
    assert mock_print.mock_calls == [call("Please enter a whole number.\n")]


def test_check_blackjack():
    player_cards = ['A', 'K']
    croupier_cards = ['A', 3]
    player_chips = 100
    player_bet = 10
    player_chips, blackjack = check_blackjack(player_cards, croupier_cards,
                                              player_chips, player_bet)
    assert player_chips == 115
    assert blackjack is True


def test_check_blackjack_2():
    player_cards = ['A', 5]
    croupier_cards = ['A', 10]
    player_chips = 100
    player_bet = 10
    player_chips, blackjack = check_blackjack(player_cards, croupier_cards,
                                              player_chips, player_bet)
    assert player_chips == 90
    assert blackjack is True


def test_check_blackjack_3():
    player_cards = ['A', 'K']
    croupier_cards = ['A', 'J']
    player_chips = 100
    player_bet = 10
    player_chips, blackjack = check_blackjack(player_cards, croupier_cards,
                                              player_chips, player_bet)
    assert player_chips == 100
    assert blackjack is True


def test_check_blackjack_4():
    player_cards = ['A', 'A']
    croupier_cards = ['A', 'A']
    player_chips = 100
    player_bet = 10
    player_chips, blackjack = check_blackjack(player_cards, croupier_cards,
                                              player_chips, player_bet)
    assert player_chips == 100
    assert blackjack is False


@patch('builtins.input', side_effect=['0'])
def test_player_turn(mock_input, deck):
    player_cards = ['K', 'K']
    player_bet = 10
    player_chips = 100
    player_chips, player_bust = player_turn(player_cards, deck, player_bet, player_chips)
    assert player_chips == 100
    assert player_bust is False


@patch('blackjack.random.choice', return_value='K')
@patch('builtins.input', side_effect=['1'])
def test_player_turn_2(mock_input, mock_choice, deck):
    player_cards = ['K', 'K']
    player_bet = 10
    player_chips = 100
    player_chips, player_bust = player_turn(player_cards, deck, player_bet, player_chips)
    assert player_chips == 90
    assert player_bust is True


@patch('blackjack.random.choice', return_value='Q')
@patch('builtins.input', side_effect=['1', '0'])
def test_player_turn_3(mock_input, mock_choice, deck):
    player_cards = ['K']
    player_bet = 10
    player_chips = 100
    player_chips, player_bust = player_turn(player_cards, deck, player_bet, player_chips)
    assert player_chips == 100
    assert player_bust is False


@patch('blackjack.random.choice', side_effect=[9, 5])
@patch('builtins.input', side_effect=['1', '1', '0'])
def test_player_turn_4(mock_input, mock_choice, deck):
    player_cards = [2, 2]
    player_bet = 10
    player_chips = 100
    player_chips, player_bust = player_turn(player_cards, deck, player_bet, player_chips)
    assert player_chips == 100
    assert player_bust is False


@patch('builtins.print')
@patch('builtins.input', side_effect=['2', '0'])
def test_player_turn_error(mock_input, mock_print, deck):
    player_cards = [5, 3]
    player_bet = 10
    player_chips = 100
    player_chips, player_bust = player_turn(player_cards, deck, player_bet, player_chips)
    assert player_chips == 100
    assert player_bust is False
    assert mock_print.mock_calls == [call('Hand value is: 8'),
                                     call("Invalid option."), call('Hand value is: 8')]


@patch('builtins.print')
@patch('builtins.input', side_effect=['hi', '0'])
def test_player_turn_nan(mock_input, mock_print, deck):
    player_cards = [5, 3]
    player_bet = 10
    player_chips = 100
    player_chips, player_bust = player_turn(player_cards, deck, player_bet, player_chips)
    assert player_chips == 100
    assert player_bust is False
    assert mock_print.mock_calls == [call('Hand value is: 8'),
                                     call("Wrong command entered, please try again."),
                                     call('Hand value is: 8')]


# More cards to test if the croupier stops at 17
@patch('blackjack.random.choice', side_effect=['K', 'K', 'K'])
def test_croupier_turn(deck):
    croupier_cards = ['K', 7]
    croupier_cards = croupier_turn(croupier_cards, deck)
    assert croupier_cards == ['K', 7]


# More cards to test if the croupier takes more than necessary
@patch('blackjack.random.choice', side_effect=['K', 'K', 'K'])
def test_croupier_turn_2(deck):
    croupier_cards = ['K', 6]
    croupier_cards = croupier_turn(croupier_cards, deck)
    assert croupier_cards == ['K', 6, 'K']


def test_winner():
    player_cards = ['K', 7]
    croupier_cards = ['K', 7]
    player_bet = 10
    player_chips = 100
    player_chips = winner(player_cards, croupier_cards, player_bet, player_chips)
    assert player_chips == 100


def test_winner_2():
    player_cards = ['K', 9, 'A']
    croupier_cards = ['K', 8]
    player_bet = 10
    player_chips = 100
    player_chips = winner(player_cards, croupier_cards, player_bet, player_chips)
    assert player_chips == 110


def test_winner_3():
    player_cards = ['K', 9]
    croupier_cards = ['K', 8, 'A', 'A', 'A']
    player_bet = 10
    player_chips = 100
    player_chips = winner(player_cards, croupier_cards, player_bet, player_chips)
    assert player_chips == 90


@patch('builtins.input', side_effect=['1'])
def test_play_again(mock_input):
    assert play_again() == 1


@patch('builtins.input', side_effect=['0'])
def test_play_again_2(mock_input):
    assert play_again() == 0


@patch('builtins.print')
@patch('builtins.input', side_effect=['15', '0'])
def test_play_again_error(mock_input, mock_print):
    play_again()
    assert mock_print.mock_calls == [call("Sorry, that option is not available.")]


@patch('builtins.print')
@patch('builtins.input', side_effect=['hi', '0'])
def test_play_again_nan(mock_input, mock_print):
    play_again()
    assert mock_print.mock_calls == [call("Please enter an integer number.\n")]
