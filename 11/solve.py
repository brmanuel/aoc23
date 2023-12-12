
import click

def read(infile):
    def get_expansion_map(indices_with_galaxies, n):
        indices_without_galaxies = sorted(set(range(n)) - set(indices_with_galaxies))
        expansion = {}
        last_i = 0
        for num, i in enumerate(indices_without_galaxies):
            for j in range(last_i, i):
                expansion[j] = num
            last_i = i
        for j in range(last_i, n):
            expansion[j] = len(indices_without_galaxies)
        return expansion

    galaxies = []
    with open(infile, "r", encoding="utf-8") as f:
        lines = list(f)
        n = len(lines)
        for i, ln in enumerate(lines):
            line = ln.rstrip()
            m = len(line)
            for j, char in enumerate(line):
                if char == "#":
                    galaxies.append((i,j))
    
    row_expansion = get_expansion_map(
        set(i for i,_ in galaxies), n
    )
    col_expansion = get_expansion_map(
        set(j for _,j in galaxies), m
    )
    return galaxies, row_expansion, col_expansion
    
def solve(input, expand):
    galaxies, row_expansion, col_expansion = input
    sum = 0
    for idx1 in range(len(galaxies)):
        i1, j1 = galaxies[idx1]
        for idx2 in range(idx1 + 1, len(galaxies)):
            i2, j2 = galaxies[idx2]
            sum += abs(
                expand(i1, row_expansion)
                - expand(i2, row_expansion)
            ) + abs(
                expand(j1, col_expansion)
                - expand(j2, col_expansion)
            )
    return sum

def expansion1(pos, expansion_map):
    return pos + expansion_map[pos]

def expansion2(pos, expansion_map):
    return pos + 999999 * expansion_map[pos]


@click.command()
@click.argument("infile")
def main(infile):
    input = read(infile)
    sol = solve(input, expansion1)
    print(sol)
    sol = solve(input, expansion2)
    print(sol)

if __name__ == "__main__":
    main()