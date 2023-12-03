
import click


def read(infile):
    input = {}
    with open(infile, "r", encoding="utf-8") as f:
        for i,line in enumerate(f):
            for j,c in enumerate(line.strip()):
                input[(i,j)] = c
    return input


def get_symbol_map(input, filter):
    symbols = []
    i_max = max(i for i,_ in input)
    j_max = max(j for _,j in input)
    for i in range(i_max+1):
        for j in range(j_max+1):
            if filter(input[(i,j)]):
                symbols.append((i,j))
    return symbols

def is_number(c):
    return c in "0123456789"
    
def is_symbol(c):
    return not is_number(c) and c != '.'

def is_gear_symbol(c):
    return c == '*'

def should_merge(number, number_range):
    i,j = number
    a,b,c,d = number_range
    return i == a and i == c and j == d+1

def touches_symbol(merged_number, symbols):
    i, start_j, _, end_j = merged_number
    return any((a,b) in symbols for a in [i-1, i, i+1] for b in range(start_j-1, end_j+2))

def read_number(merged_number, input):
    i, start_j, _, end_j = merged_number
    num = 0
    for j in range(start_j, end_j+1):
        num *= 10
        num += int(input[(i,j)])
    return num


def merge_adjacent_coords(coords):        
    coords_merged = [[coords[0][0], coords[0][1], coords[0][0], coords[0][1]]]
    for coord in coords[1:]:
        if should_merge(coord, coords_merged[-1]):
            coords_merged[-1][2] = coord[0]
            coords_merged[-1][3] = coord[1]
        else:
            coords_merged.append([coord[0],coord[1],coord[0],coord[1]])
    return coords_merged


def solve1(input):        
    symbols = get_symbol_map(input, is_symbol)
    numbers = get_symbol_map(input, is_number)
    numbers_merged = merge_adjacent_coords(numbers)
    
    sum = 0
    for merged_number in numbers_merged:
        if touches_symbol(merged_number, symbols):
            sum += read_number(merged_number, input)
    return sum


def solve2(input):
    gear_symbols = get_symbol_map(input, is_gear_symbol)
    numbers = get_symbol_map(input, is_number)
    numbers_merged = merge_adjacent_coords(numbers)

    sum = 0
    for gear in gear_symbols:
        numbers_touched = [
            number for number in numbers_merged
            if touches_symbol(number, [gear])
        ]
        if len(numbers_touched) == 2:
            num1, num2 = numbers_touched
            sum += read_number(num1, input) * read_number(num2, input)
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
