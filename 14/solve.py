import click 
from pprint import pprint

def read(infile):
    input = []
    with open(infile, "r", encoding="utf-8") as f:
        for line in f:
            input.append(list(line.rstrip()))
    return input

def solve(input):
    sum = 0
    initial_limit = len(input)
    limits = [initial_limit] * len(input[0])
    for i, line in enumerate(input):
        for j, char in enumerate(line):
            if char == "#":
                limits[j] = initial_limit - i - 1
            if char == "O":
                sum += limits[j]
                limits[j] -= 1
    return sum

def simulate(round_rocks, cube_rocks, n, m, direction):
    
    def transform(rock):
        i,j = rock
        if direction == "up":
            return (i,j)
        if direction == "down":
            return (n-i, j)
        if direction == "left":
            return (j, i)
        return (m-j, i)
    
    def transform_back(rock):
        i,j = rock
        if direction == "up":
            return (i,j)
        if direction == "down":
            return (n-i, j)
        if direction == "left":
            return (j, i)
        return (j, m-i)

    round_rocks = set(transform(rock) for rock in round_rocks)
    cube_rocks = set(transform(rock) for rock in cube_rocks)

    round_lines = {}
    cube_lines = {}
    for rocks, lines in [(round_rocks, round_lines), (cube_rocks, cube_lines)]:
        for i,j in rocks:
            if j not in lines:
                lines[j] = set()
            lines[j].add((i,j))


    new_round_rocks = set()
    for line_idx in round_lines:
        round_line = sorted(round_lines[line_idx])
        cube_line = sorted(cube_lines.get(line_idx, set()))
        cube_line.append((99999999999999, line_idx))
        cube_idx = 0
        round_idx = 0
        stack = 0

        while round_idx < len(round_line):
            round_rock = round_line[round_idx]
            cube_rock = cube_line[cube_idx]
            if round_rock < cube_rock:
                new_round_rocks.add(transform_back((stack, line_idx)))
                round_idx += 1
                stack += 1
            else:
                cube_idx += 1
                stack = cube_rock[0] + 1
    return new_round_rocks
   
    
def solve2(input):
    def one_round(round_rocks):
        round_rocks = simulate(round_rocks, cube_rocks, n, m, "up")
        round_rocks = simulate(round_rocks, cube_rocks, n, m, "left")
        round_rocks = simulate(round_rocks, cube_rocks, n, m, "down")
        round_rocks = simulate(round_rocks, cube_rocks, n, m, "right")
        return round_rocks
    
    n = len(input)-1
    m = len(input[0])-1
    round_rocks = set()
    cube_rocks = set()
    for i, line in enumerate(input):
        for j, char in enumerate(line):
            if char == "#":
                cube_rocks.add((i,j))
            if char == "O":
                round_rocks.add((i,j))

    state_to_round = {}
    round_to_state = {}
    round = 0
    while True:
        state = tuple(sorted(round_rocks))
        if state in state_to_round:
            cycle_start = state_to_round[state]
            cycle_length = round - cycle_start
            print(round, cycle_start, cycle_length)
            break
        state_to_round[state] = round
        round_to_state[round] = state
        round += 1
        round_rocks = one_round(round_rocks)

    cycles = 1000000000
   
    round_rocks = round_to_state[cycle_start + ((cycles - cycle_start) % cycle_length)]
    load = sum(len(input) - i for i,_ in round_rocks)
    return load



@click.command()
@click.argument("infile")
def main(infile):
    input = read(infile)
    sol = solve2(input)
    print(sol)
    
if __name__ == "__main__":
    main()