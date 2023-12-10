import click

def read(infile):
    input = []
    with open(infile, "r", encoding="utf-8") as f:
        for line in f:
            cards, bid = line.rstrip().split()
            input.append((list(cards), int(bid)))
    return input


    
def sorting_function_1(hand):
    # map hand to tuple of occurrences of each card, sorted in descending order
    # plus the cards of the hand in the order they appear
    def card_value(card):
        value_map = {
            "T": 10,
            "J": 11,
            "Q": 12,
            "K": 13,
            "A": 14,
        }
        if card in value_map:
            return value_map[card]
        return int(card)

    occurrences = {}
    for card in hand:
        if card not in occurrences:
            occurrences[card] = 0
        occurrences[card] += 1
    return sorted(occurrences.values(), reverse=True) + [card_value(card) for card in hand]

def sorting_function_2(hand):
    def card_value(card):
        value_map = {
            "J": 1,
            "T": 10,
            "Q": 12,
            "K": 13,
            "A": 14,
        }
        if card in value_map:
            return value_map[card]
        return int(card)

    occurrences = {}
    for card in hand:
        if card not in occurrences:
            occurrences[card] = 0
        occurrences[card] += 1
    
    j_occurrences = occurrences.get("J", 0)
    if j_occurrences == 0:
        sorted_occurrences = sorted(occurrences.values(), reverse=True)
    elif j_occurrences == 5:
        sorted_occurrences = [5]
    else:
        del occurrences["J"]
        sorted_occurrences = sorted(occurrences.values(), reverse=True)
        sorted_occurrences[0] += j_occurrences
        
    return sorted_occurrences + [card_value(card) for card in hand]



def solve(input, sorting_function):
    input_sorted = sorted(input, key = lambda line: sorting_function(line[0]))
    sum = 0
    for i, (_, bid) in enumerate(input_sorted):
        sum += bid * (i+1)
    return sum


@click.command()
@click.argument("infile")
def main(infile):
    input = read(infile)
    sol = solve(input, sorting_function_1)
    print(sol)
    sol = solve(input, sorting_function_2)
    print(sol)

if __name__ == "__main__":
    main()