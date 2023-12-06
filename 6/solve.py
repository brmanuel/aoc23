import click


def read(infile):
    with open(infile, "r", encoding="utf-8") as f:
        times = [int(time) for time in f.readline().split(":")[1].strip().split()]
        dists = [int(dist) for dist in f.readline().split(":")[1].strip().split()]
        return list(zip(times, dists))

def sum_naive(time, dist):
    sum = 0
    for load_time in range(time+1):
        if load_time * (time - load_time) > dist:
            sum += 1
    return sum


def sum_binary(time, dist):
    def large_enough(load_time):
        return load_time * (time - load_time) > dist
    
    lb = 0
    ub = round(time / 2)
    while lb +1 < ub:
        mid = round((lb + ub) / 2)
        if large_enough(mid):
            ub = mid
        else:
            lb = mid
    return time+1 - 2*ub


def solve1(input):
    prod = 1
    for time, dist in input:
        prod *= sum_binary(time, dist)        
    return prod

def solve2(input):
    comb_time = int("".join(str(time) for time, _ in input))
    comb_dist = int("".join(str(dist) for _, dist in input))
    return sum_binary(comb_time, comb_dist)


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