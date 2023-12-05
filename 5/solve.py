
import click

SECTIONS = [
    "seed-to-soil",
    "soil-to-fertilizer",
    "fertilizer-to-water",
    "water-to-light",
    "light-to-temperature",
    "temperature-to-humidity",
    "humidity-to-location",
]


def read(infile):
    sections = {
        section: {} for section in SECTIONS
    }
    seeds = []
    with open(infile, "r", encoding="utf-8") as f:
        line = f.readline().rstrip()
        seeds = list(int(seed) for seed in line.split(":")[1].split())
        mapping = None
        for line in f:
            splitted = line.split()
            if len(splitted) == 0:
                continue
            elif splitted[0] in sections:
                mapping = sections[splitted[0]]
            else:
                assert mapping is not None
                dst_start, src_start, length = map(int, splitted)
                mapping[(src_start, src_start+length-1)] = (dst_start, dst_start+length-1)
    return seeds, sections

def get_location_of_seed(seed, sections):
    value = seed
    for section in SECTIONS:
        mapping = sections[section]
        next_value = value
        for (src_lb,src_ub), (dst_lb, dst_ub) in mapping.items():
            if src_lb <= value <= src_ub:
                next_value = dst_lb + value - src_lb
                break
        value = next_value
    return value

def solve1(input):
    seeds, sections = input
    min_location = None
    for seed in seeds:
        location = get_location_of_seed(seed, sections)        
        if min_location is None or location < min_location:
            min_location = location
    return min_location


def solve2(input):
    seed_ranges, sections = input
    min_location = None
    for seed_start, length in zip(seed_ranges[::2], seed_ranges[1::2]):
        seed = seed_start
        while seed < seed_start + length:
            seed_increment = None
            value = seed
            for section in SECTIONS:
                mapping = sections[section]
                next_value = value
                for (src_lb,src_ub), (dst_lb, dst_ub) in mapping.items():
                    if src_lb <= value <= src_ub:
                        next_value = dst_lb + value - src_lb
                        increment = src_ub - value + 1
                        if seed_increment is None:
                            seed_increment = increment
                        seed_increment = min(seed_increment, increment)
                        break
                value = next_value
            location = value      
            seed += seed_increment
            if min_location is None or location < min_location:
                min_location = location
    return min_location


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