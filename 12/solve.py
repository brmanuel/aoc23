import click

def read(infile):
    lines = []
    with open(infile, "r", encoding="utf-8") as f:
        for line in f:
            pattern, numbers = line.rstrip().split()
            lines.append((pattern, [int(num) for num in numbers.split(",")]))

    return lines

def multiply(input):
    num = 5
    input_mul = []
    for pattern, numbers in input:
        input_mul.append((
            "?".join([pattern] * num),
            numbers * num
        ))
    return input_mul


def solve(input):
    dp = {}
    def num_options_in_group(group, numbers):
        sum = 0
        if len(numbers) == 0:
            if "#" in group:
                return 0
            return 1
        
        if (group, tuple(numbers)) not in dp:
            number = numbers[0]
            max_idx = len(group) - number
            if "#" in group:
                max_idx = min(group.index("#"), max_idx)

            for idx in range(max_idx+1):
                if len(group) > idx+number and group[idx+number] == "#":
                    continue
                sum += num_options_in_group(group[idx+number+1:], numbers[1:])
            dp[(group, tuple(numbers))] = sum
        return dp[(group, tuple(numbers))]

    
    dp2 = {}
    def solve_rec(groups, numbers):
        sum = 0
        if len(groups) == 0:
            if len(numbers) == 0:
                return 1
            return 0
        
        if (tuple(groups), tuple(numbers)) not in dp2:
            group =  groups[0]
            for idx in range(len(numbers)+1):
                numbers_for_group = numbers[:idx]
                options_for_group_and_numbers = num_options_in_group(group, numbers_for_group)
                sum += options_for_group_and_numbers * solve_rec(
                    groups[1:], numbers[idx:]
                )
            dp2[(tuple(groups), tuple(numbers))] = sum
        return dp2[(tuple(groups), tuple(numbers))]

    sol = 0
    for pattern, numbers in input:
        groups = [grp for grp in pattern.split(".") if len(grp) > 0]
        increment = solve_rec(groups, numbers)
        sol += increment
    return sol


@click.command()
@click.argument("infile")
def main(infile):
    input = read(infile)
    input2 = multiply(input)
    sol = solve(input)
    print(sol)
    sol = solve(input2)
    print(sol)

if __name__ == "__main__":
    main()