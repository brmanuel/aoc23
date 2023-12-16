import click

def read(infile):
    input = []
    with open(infile, "r", encoding="utf-8") as f:
        for line in f:
            input.append(list(line.rstrip()))
    return input


def simulate(input, initial):
    def is_outside(x,y):
        return x < 0 or x >= len(input) or y < 0 or y >= len(input)
    
    def refract(x,y,dx,dy):
        assert dx*dy == 0 and abs(dx+dy) == 1
        if dx != 0:
            return [((x,y+1),(0,1)), ((x,y-1),(0,-1))]
        return [((x+1,y),(1,0)), ((x-1,y),(-1,0))]
    
    def mirror(x,y,dx,dy,char):
        if char == "\\":
            new_dir = (dy,dx)
        else:
            new_dir = (-dy,-dx)
        return [((x+new_dir[0], y+new_dir[1]), new_dir)]

        
    seen = set()
    queue = [initial]
    while len(queue) > 0:
        (x,y), (dx, dy) = queue.pop(0)
        if ((x,y),(dx,dy)) in seen or is_outside(x,y):
            continue
        seen.add(((x,y),(dx,dy)))
        char = input[x][y]
        if char == "." or char == "-" and dx == 0 or char == "|" and dy == 0:
            queue.append(((x+dx,y+dy), (dx,dy)))
        elif char == "-" and dx != 0 or char == "|" and dy != 0:
            queue += refract(x,y,dx,dy)
        elif char == "/" or char == "\\":
            queue += mirror(x,y,dx,dy,char)
    num_seen = len(set((x,y) for ((x,y),_) in seen))
    return num_seen

def solve1(input):
    return simulate(input, ((0, 0), (0,1)))

def solve2(input):
    max_covered = 0
    n = len(input)
    m = len(input[0])
    for i in range(n):
        num_covered = simulate(input, ((i,0),(0,1)))
        max_covered = max(max_covered, num_covered)
        num_covered = simulate(input, ((i,m-1),(0,-1)))
        max_covered = max(max_covered, num_covered)
    for j in range(m):
        num_covered = simulate(input, ((0,j),(1,0)))
        max_covered = max(max_covered, num_covered)
        num_covered = simulate(input, ((i,n-1),(-1,0)))
        max_covered = max(max_covered, num_covered)
    return max_covered


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