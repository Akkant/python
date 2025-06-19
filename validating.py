def get_number():
    while True:
        value = input("Enter a number: ")
        if value.isdigit():
            return int(value)
        else:
            print("That's not a valid number.")
