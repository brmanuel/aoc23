import click

def read(infile):
    instructions = []
    with open(infile, "r", encoding="utf-8") as f:
        for line in f:
            dir, num, _ = line.rstrip().split()
            instructions.append((dir, int(num)))
    return instructions

def read2(infile):
    instructions = []
    with open(infile, "r", encoding="utf-8") as f:
        for line in f:
            _,_, rgb = line.rstrip().split()
            num = int(rgb[2:-2], 16)
            dir = ["R", "D", "L", "U"][int(rgb[-2])]
            instructions.append((dir, num))
    return instructions


def insert(active_lines, line):
    def subtract(ll1, ll2):
        # subtract ll1 from ll2
        ll1a, ll1b = sorted(ll1)
        ll2a, ll2b = sorted(ll2)
        if ll1b <= ll2a:
            return [tuple(sorted((ll2a, ll2b)))]
        if ll2b <= ll1a:
            return [tuple(sorted((ll2a, ll2b)))]
        if ll1a == ll2a and ll2b == ll1b:
            return []
        if ll1a > ll2a and ll2b > ll1b:
            return [tuple(sorted((ll2a, ll1a))), tuple(sorted((ll1b,ll2b)))]
        if ll1a == ll2a:
            assert ll1b < ll2b
            return [tuple(sorted((ll1b, ll2b)))]
        if ll1b == ll2b:
            assert ll1a > ll2a
            return [tuple(sorted((ll2a, ll1a)))]
        assert False

    new_active_lines = []
    for l in active_lines:
        new_active_lines += subtract(line, l)
    if new_active_lines == active_lines:
        new_active_lines += [tuple(sorted(line))]
    return new_active_lines


def merge(lines):
    if len(lines) == 0:
        return lines
    lines.sort()
    merged_lines = [lines[0]]
    for line in lines[1:]:
        if line[0] <= merged_lines[-1][1]:
            merged_lines[-1] = (merged_lines[-1][0], max(merged_lines[-1][-1], line[1]))
        else:
            merged_lines.append(line)
    return merged_lines

def solve(input):
    def step(coord, dir, num):
        if dir == "R":
            return (coord[0], coord[1] + num)
        if dir == "D":
            return (coord[0] + num, coord[1])
        if dir == "U":
            return (coord[0] - num, coord[1])
        if dir == "L":
            return (coord[0], coord[1] - num)
        
    def get_y(line):
        (x1,y1),(x2,y2) = line
        return y1

        
    def length(active_lines):
        merged_lines = merge(active_lines)
        sum = 0
        for lb,ub in merged_lines:
            sum += ub - lb + 1
        return sum

    h_lines = []
    v_lines = []
    coord = (0,0)
    for dir,num in input:
        new_coord = step(coord, dir, num)
        if new_coord[0] == coord[0]:
            h_lines.append((coord, new_coord))
        else:
            v_lines.append((coord, new_coord))
        coord = new_coord
    
    sum = 0
    v_lines_dict = {}
    for line in v_lines:
        if get_y(line) not in v_lines_dict:
            v_lines_dict[get_y(line)] = []
        v_lines_dict[get_y(line)].append(tuple(sorted((line[0][0], line[1][0]))))

    points = list(range(min(v_lines_dict), max(v_lines_dict)+1))
    active_lines = []
    for p in points:
        for line in v_lines_dict.get(p, []):
            active_lines = merge(insert(active_lines, line))
        inc = length(active_lines + v_lines_dict.get(p, []))
        sum += inc

    return sum
        


@click.command()
@click.argument("infile")
def main(infile):
    input = read(infile)
    sol = solve(input)
    print(sol)
    input = read2(infile)
    sol = solve(input)
    print(sol)
    
if __name__ == "__main__":
    main()