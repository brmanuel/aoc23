import click
from heapq import heappush, heappop

def read(infile):
    input = []
    with open(infile, "r", encoding="utf-8") as f:
        for line in f:
            input.append([int(c) for c in line.rstrip()])
    return input


def possible_directions1(last_move, num_last_move):
    all_directions = [(0,1), (1,0), (0,-1), (-1,0)]
    if last_move in all_directions:
        inverse_move = (-last_move[0], -last_move[1])
        all_directions.remove(inverse_move)
    if num_last_move >= 3:
        all_directions.remove(last_move)
    return all_directions

def possible_directions2(last_move, num_last_move):
    all_directions = [(0,1), (1,0), (0,-1), (-1,0)]
    if last_move in all_directions:
        inverse_move = (-last_move[0], -last_move[1])
        all_directions.remove(inverse_move)
    if last_move in all_directions and num_last_move < 4:
        all_directions = [last_move]
    if num_last_move >= 10:
        all_directions.remove(last_move)
    return all_directions


def solve(input, possible_directions):
    n = len(input)-1
    m = len(input[0])-1
    source = (0,0)
    target = (n,m)

    seen = set()
    queue = [(0, source, "", 0)]
    while len(queue) > 0:
        next = heappop(queue)
        heat_loss, position, last_move, num_last_move = next
        if (position,last_move,num_last_move) in seen:
            continue
        seen.add((position,last_move,num_last_move))
        # Need to uncomment num_last_move >= 4 for subproblem 2
        if position == target: #and num_last_move >= 4:
            return heat_loss
        
        for direction in possible_directions(last_move, num_last_move):
            next_pos = (position[0] + direction[0], position[1] + direction[1])
            if next_pos[0] < 0 or next_pos[0] > n or next_pos[1] < 0 or next_pos[1] > m:
                continue
            next_heat_loss = heat_loss + input[next_pos[0]][next_pos[1]]
            if direction == last_move:
                next_num_last_move = num_last_move+1
            else:
                next_num_last_move = 1
            heappush(queue, (next_heat_loss, next_pos, direction, next_num_last_move))


@click.command()
@click.argument("infile")
def main(infile):
    input = read(infile)
    sol = solve(input, possible_directions2)
    print(sol)
    
if __name__ == "__main__":
    main()