def game():
    print("Guess a number between 1 and 10")
    secret = 7
    guess = int(input("Your guess: "))
    if guess == secret:
        print("Correct!")
    else:
        print("Try again!")

game()