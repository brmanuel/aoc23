import click

def read(infile):
    with open(infile, "r", encoding="utf-8") as f:
        line = f.readline().rstrip().split(",")
        return line
    

def hash_alg(str):
    sum = 0
    for c in str:
        sum += ord(c)
        sum *= 17
        sum %= 256
    return sum

def solve(input):
    sum = 0
    for str in input:
        sum += hash_alg(str)
    return sum

def solve2(input):
    def get_box(step):
        return hash_alg(get_label(step))
    
    def get_label(step):
        op = get_op(step)
        return step.split(op)[0]
    
    def get_focal(step):
        assert get_op(step) == "="
        return int(step.split("=")[1])

    def get_op(step):
        if "=" in step:
            return "="
        return "-"

    boxes = {i: [] for i in range(256)}
    for str in input:
        box = get_box(str)
        if get_op(str) == "=":
            found = False
            for lens in boxes[box]:
                if lens[0] == get_label(str):
                    found = True
                    lens[1] = get_focal(str)
            if not found:
                boxes[box].append([get_label(str), get_focal(str)])
        else:
            boxes[box] = [
                lens for lens in boxes[box]
                if lens[0] != get_label(str)
            ]


    sum = 0
    for i,box in boxes.items():
        for j,lens in enumerate(box):
            sum += (i+1) * (j+1) * lens[1]
    return sum








@click.command()
@click.argument("infile")
def main(infile):
    input = read(infile)
    sol = solve(input)
    print(sol)
    sol = solve2(input)
    print(sol)
    
if __name__ == "__main__":
    main()