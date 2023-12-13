import click

def read(infile):
    rows = []
    cols = []
    instances = []
    with open(infile, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if len(stripped) == 0:
                instances.append((rows, cols))
                rows = []
                cols = []
                continue
            rows.append(stripped)
            if len(cols) == 0:
                cols = list(stripped)
            else:
                cols = [col + char for col,char in zip(cols, stripped)]
        instances.append((rows, cols))
    return instances

def find_mirror_axes_1(lines):
    candidates = set(range(1, len(lines)))
    for i in range(len(lines)):
        #print(i, lines[i])
        for j in range(i+1, len(lines), 2):
            impossible_mirror = (i+j) // 2 + 1
            if lines[i] != lines[j] and impossible_mirror in candidates:
                #print("removes", impossible_mirror, "with", j, lines[j])
                candidates.remove(impossible_mirror)
    return list(candidates)

def find_mirror_axes_2(lines):
    def diff(line1, line2):
        return [k for k,(c1, c2) in enumerate(zip(line1, line2)) if c1 != c2]

    axes = []
    candidates = set(range(1, len(lines)))
    for c in candidates:
        smudges = []
        for i in range(c):
            j = c + (c - i) - 1
            if j >= len(lines):
                continue
            for d in diff(lines[i], lines[j]):
                smudges.append(set([(i, d), (j,d)]))
        # check if smudges can be united
        
        if len(smudges) == 1:
            axes.append(c)
        elif len(smudges) > 0:
            smudge = smudges[0]
            for s in smudges[1:]:
                smudge &= s
            if len(smudge) == 1:
                axes.append(c)
    return axes


def solve(input, find_mirror_axes):
    sum = 0
    for rows, cols in input:
        row_mirror = find_mirror_axes(rows)
        col_mirror = find_mirror_axes(cols)
        assert len(row_mirror) + len(col_mirror) == 1
        if len(row_mirror) == 1:
            sum += 100 * row_mirror[0]
        else:
            sum += col_mirror[0]
    return sum


@click.command()
@click.argument("infile")
def main(infile):
    input = read(infile)
    sol = solve(input, find_mirror_axes_1)
    print(sol)
    sol = solve(input, find_mirror_axes_2)
    print(sol)
    
if __name__ == "__main__":
    main()