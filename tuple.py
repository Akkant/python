def stats(numbers):
    return min(numbers), max(numbers)

low, high = stats([1, 2, 3, 4])
print(low, high)