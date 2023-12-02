
import click

def read_infile(infile):
    with open(infile, "r", encoding="utf-8") as f:
        return [list(line.rstrip()) for line in f]


def solve(input, numbers):
    sum = 0
    for line in input:
        minidx = len(line)
        linestr = "".join(line)
        maxidx = -1
        first = None
        last = None
        for str, num in numbers.items():
            idx = linestr.find(str)
            if 0 <= idx < minidx:
                minidx = idx
                first = num
            idx = linestr.rfind(str)
            if maxidx < idx:
                maxidx = idx
                last = num
        sum += 10*first + last
    return sum

def solve2(input):
    return solve(input, {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
    })

def solve1(input):
    return solve(input, {
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
    })
    

@click.command()
@click.argument("infile")
def main(infile):
    input = read_infile(infile)
    sol = solve1(input)
    print(sol)
    sol = solve2(input)
    print(sol)


if __name__ == "__main__":
    main()