import click
import re

def read(infile):
    line_pattern = re.compile("(.*) = \((.*), (.*)\)")
    with open(infile, "r", encoding="utf-8") as f:
        instructions = list(f.readline().rstrip())
        graph = {}
        f.readline()
        for line in f:
            m = line_pattern.match(line)
            if m is not None:
                graph[m.group(1)] = {"L": m.group(2), "R": m.group(3)}
        return instructions, graph


def solve(instructions, graph, start, is_end):
    def make_step(current, instr):
        return graph[current][instructions[instr % len(instructions)]]
    
    visited = set()
    current = make_step(start, 0)
    instr = 1
    while not is_end(current):
        visited.add((current, instr % len(instructions)))
        current = make_step(current, instr)
        instr += 1
        if (current, instr % len(instructions)) in visited:
            instr = None
            break
    return instr, current


def solve1(input):
    instructions, graph = input
    num_instr, _ = solve(instructions, graph, "AAA", lambda x: x == "ZZZ")
    return num_instr

def solve2(input):
    instructions, graph = input

    start_to_num_dict = {}
    def start_to_num(start, idx):
        if (start, idx) not in start_to_num_dict:
            num = solve(instructions[idx:] + instructions[:idx], graph, start, lambda x: x.endswith("Z"))
            start_to_num_dict[(start, idx)] = num
        return start_to_num_dict[(start, idx)]

    current_nodes = []
    current_steps = []
    for node in graph:
        if node.endswith("A"):
            instr, next_node = start_to_num(node, 0)
            current_nodes.append(next_node)
            current_steps.append(instr)
     
    min_size = 100
    while len(set(current_steps)) > 1:
        if len(set(current_steps)) < min_size:
            min_size = len(set(current_steps))
            print(min_size)
        min_steps, min_idx = min((steps, idx) for idx, steps in enumerate(current_steps))
        print(min_steps)
        min_node = current_nodes[min_idx]
        next_steps, next_node = start_to_num(min_node, min_idx % len(instructions))
        current_steps[min_idx] += next_steps
        current_nodes[min_idx] = next_node
    return current_steps[0]


def ggt(a,b):
    if a == b:
        return a
    if a < b:
        return ggt(a, b-a)
    else:
        return ggt(a-b, b)
    

def crt(modulos, remainders):
    can_apply_crt = all(
        r1 % ggt(m1, m2) == r2 % ggt(m1, m2)
        for r1,m1 in zip(remainders, modulos)
        for r2,m2 in zip(remainders, modulos)
        if (r1, m1) != (r2, m2)
    )
    assert can_apply_crt



def solve3(input):
    instructions, graph = input

    starts = [node for node in graph if node.endswith("A")]
    
    def make_step(current, instr):
        return graph[current][instructions[instr % len(instructions)]]

    cycles = []
    for start in starts:
        seen = {}
        current = make_step(start, 0)
        instr = 1
        ends = []
        while (current, instr % len(instructions)) not in seen: # or (instr % len(instructions)) != 0:
            seen[(current, instr % len(instructions))] = instr
            current = make_step(current, instr)
            if current.endswith("Z"):
                ends.append((current, instr))
            instr += 1

        idx = seen[(current, instr % len(instructions))]
        cycles.append({
            "start": idx,
            "length": instr - idx,
            "ends": ends
        })
    
    all_end_combinations = 
    n = crt(
        [c["length"] for c in cycles],
        [c[""]]
    )

    
    # the instruction id n where all paths are at an end
    # is given by the system of mod kongruences
    # n % length(i) = end(i)
    # add 1 to it to get the length of the sequence
    





# 22a, 0
# 22b, 1 <-+
# 22c, 0   |
# 22z, 1   |
# 22b, 0   |
# 22c, 1   |
# 22z, 0 --+


    

# cba -> (dgh, dgz)

# s -------> x --> x -> x ---> x --------------> x ------------> s
# s ----> x -----> x -----------------> x --------------> s

# each cycle c has a length l(c)
# in each cycle, there are E(c) ENDS, at positions e(c,1), e(c,2), ..., e(c, E(c))
# all ends of this cycle are thus on positions Xc * l(c) + e(c, Yc) for Xc a positive integer and Yc in [1,..., E(c)]

# find n s.t. n % l(c) is an END for all cycles c

# say we know which END e(c) will be chosen for every cycle, then
# find n s.t. n % l(c) = e(c) for all c




@click.command()
@click.argument("infile")
def main(infile):
    input = read(infile)
    # sol = solve1(input)
    # print(sol)
    sol = solve3(input)
    print(sol)

if __name__ == "__main__":
    main()