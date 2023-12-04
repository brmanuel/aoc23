
import click

def read(infile):
    cards = []
    with open(infile, "r", encoding="utf-8") as f:
        for line in f:
            _, numbers = line.strip().split(":")
            win_numbers, my_numbers = numbers.split("|")
            cards.append({
                "win_numbers": [int(num) for num in win_numbers.split()],
                "my_numbers": [int(num) for num in my_numbers.split()]
            })
    return cards

    

def solve1(input):
    def score_card(card):
        score = 0
        for num in card["my_numbers"]:
            if num in card["win_numbers"]:
                if score == 0:
                    score = 1
                else:
                    score *= 2
        return score
    
    sum = 0
    for card in input:
        sum += score_card(card)
    return sum

def solve2(input):
    def score_card(card):
        score = 0
        for num in card["my_numbers"]:
            if num in card["win_numbers"]:
                score += 1
        return score
        
    card_instances = {
        idx : 1 for idx in range(len(input))
    }
    for idx, card in enumerate(input):
        score = score_card(card)
        for copied_card in range(idx+1, idx+1+score):
            if copied_card in card_instances:
                card_instances[copied_card] += card_instances[idx]
    num_cards = sum(num_copies for num_copies in card_instances.values())
    return num_cards


@click.command()
@click.argument("infile")
def main(infile):
    input = read(infile)
    sol = solve1(input)
    print(sol)
    sol = solve2(input)
    print(sol)


if __name__ == "__main__":
    main()
