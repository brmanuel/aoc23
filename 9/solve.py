

import click

def read(infile):
    sequences = []
    with open(infile, "r", encoding="utf-8") as f:
        for line in f:
            sequences.append(
                [int(num) for num in line.rstrip().split()]
            )
    return sequences

def solve1(input):
    def extend(seq):
        if all(elem == 0 for elem in seq):
            return seq + [0]
        extended = extend([
            b - a for a,b in zip(seq, seq[1:])
        ])
        return seq + [seq[-1] + extended[-1]]
    
    sum = 0
    for seq in input:
        sum += extend(seq)[-1]
    return sum

def solve2(input):
    def extend(seq):
        if all(elem == 0 for elem in seq):
            return [0] + seq
        extended = extend([
            b - a for a,b in zip(seq, seq[1:])
        ])
        return [seq[0] - extended[0]] + seq
    
    sum = 0
    for seq in input:
        sum += extend(seq)[0]
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