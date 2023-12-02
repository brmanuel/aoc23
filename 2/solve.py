
import click

def read(infile):
    def parse_color(draw):
        # " 3 blue" -> blue
        return draw.strip().split()[1]

    def parse_num(draw):
        # 3 blue" -> 3
        return int(draw.strip().split()[0])
        
    games = {}
    with open(infile, "r", encoding="utf-8") as f:
        for line in f:
            # parse line
            # "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
            # {1: [{"blue": 3, "red": 4}, {"blue": 6, "red": 1, "green": 2}, {"green": 2}]}
            name, descr = line.rstrip().split(":")
            idx = int(name.split()[1])
            rounds = list(map(
                lambda rnd: {
                    parse_color(draw): parse_num(draw)
                    for draw in rnd.split(",")
                },
                descr.split(";")
            ))
            games[idx] = rounds
    return games
            
            

def solve1(input):
    def possible(rnd):
        return all(MAX[color] >= num for color,num in rnd.items())
        
    MAX = {
        "red": 12,
        "green": 13,
        "blue": 14
    }
    sum = 0
    for idx, rounds in input.items():
        if all(possible(rnd) for rnd in rounds):
            sum += idx
    return sum

def solve2(input):
    sum = 0
    for rounds in input.values():
        prod = 1
        for color in ["red", "green", "blue"]:
            prod *= max(rnd.get(color, 0) for rnd in rounds)
        sum += prod
    return sum


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
