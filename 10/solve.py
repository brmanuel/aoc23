
import click

def read(infile):
    def connected(char, i, j):
        char_map = {
            "|": [(i-1, j), (i+1, j)],
            "-": [(i, j-1), (i, j+1)],
            "L": [(i-1, j), (i, j+1)],
            "F": [(i+1, j), (i, j+1)],
            "7": [(i, j-1), (i+1, j)],
            "J": [(i, j-1), (i-1, j)],
        }
        return char_map.get(char, [])
    
    pipes = {}
    pipes_char = {}
    start = None
    with open(infile, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            for j, c in enumerate(line.rstrip()):
                pipes[(i,j)] = connected(c, i, j)
                pipes_char[(i,j)] = c
                if c == "S":
                    start = (i,j)

    return pipes, pipes_char, start

def find_loop_coords(input):
    pipes, _, (i, j) = input
    for next in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
        if next in pipes and (i,j) in pipes[next]:
            break
    
    start = (i,j)
    seen = set([start])
    current = next
    while True:
        seen.add(current)
        nexts = pipes[current]
        assert len(nexts) == 2
        not_seen = [next for next in nexts if next not in seen]
        if len(not_seen) == 0:
            break
        assert len(not_seen) == 1
        current = not_seen[0]
    return seen

def solve1(input):
    loop_coords = find_loop_coords(input)
    return len(loop_coords) // 2
        

def solve2(input):
    def is_inside(coord):
        dir = (-1, 0)
        obstructions = set(["J", "7", "-"])
        num_obstructions = 0
        current = coord
        while current in pipes:
            if current in loop_coords and pipes[current] in obstructions:
                num_obstructions += 1
            current = (current[0] + dir[0], current[1] + dir[1])
        return num_obstructions % 2 == 1
    
    def connect(dir, i, j):
        connects = {
            "-": ["left", "right"],
            "|": ["up", "down"],
            "7": ["left", "down"],
            "F": ["right", "down"],
            "L": ["up", "right"],
            "J": ["up", "left"],
        }
        return (i,j) in pipes and dir in connects.get(pipes[(i,j)], [])

    _, pipes, (i,j) = input
    loop_coords = find_loop_coords(input)
    if connect("up", i+1, j) and connect("down", i-1, j):
        pipes[(i,j)] = "|"
    if connect("left", i, j+1) and connect("right", i, j-1):
        pipes[(i,j)] = "-"
    if connect("left", i, j+1) and connect("up", i+1, j):
        pipes[(i,j)] = "F"
    if connect("down", i-1, j) and connect("right", i, j-1):
        pipes[(i,j)] = "J"
    if connect("down", i-1, j) and connect("left", i, j+1):
        pipes[(i,j)] = "L"
    if connect("up", i+1, j) and connect("right", i, j-1):
        pipes[(i,j)] = "7"

    num_inside = 0
    for coord in pipes:
        if coord not in loop_coords:
            if is_inside(coord):
                num_inside += 1
    return num_inside




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

