import random

def make_deck():
    cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = cards * 4  
    random.shuffle(deck)
    return deck

def get_value(card):
    if card in ['J', 'Q', 'K']:
        return 10
    if card == 'A':
        return 11
    return int(card)

def total(hand):
    total = sum(get_value(card) for card in hand)
    if total > 21 and 'A' in hand:
        total -= 10
    return total

def play():
    deck = make_deck()
    player = [deck.pop(), deck.pop()]
    dealer = [deck.pop(), deck.pop()]

    while total(player) < 21:
        print("\nYour hand:", player, "Total:", total(player))
        print("Dealer shows:", dealer[0])
        move = input("Hit or Stand? (h/s): ")
        if move == 'h':
            player.append(deck.pop())
        else:
            break

    while total(dealer) < 17:
        dealer.append(deck.pop())

    print("\nDealer hand:", dealer, "Total:", total(dealer))
    print("Your final hand:", player, "Total:", total(player))

    if total(player) > 21:
        print("You busted. Dealer wins.")
    elif total(dealer) > 21 or total(player) > total(dealer):
        print("You win!")
    elif total(player) == total(dealer):
        print("It's a tie!")
    else:
        print("Dealer wins.")

play()