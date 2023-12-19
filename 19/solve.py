import click
import re

def read(infile):
    def parse_workflow(line):
        
        # px{a<2006:qkq,m>2090:A,rfg}
        outter_pattern = re.compile("([a-z]+)\{(.*),([a-zA-Z]+)\}")
        inner_pattern = re.compile("([xmas])([<>])([0-9]+):([a-zA-Z]+),")
        outer_match = re.match(outter_pattern, line.rstrip())
        assert outer_match is not None
        name, inner, default_rule = outer_match.groups()
        rules = re.findall(inner_pattern, inner + ",")
        rule_list = [
            {"condition": (prop, comp, int(val)), "next": next}
            for prop, comp, val, next in rules
        ] + [
            {"condition": "true", "next": default_rule}
        ]
        return name, rule_list
    
    workflows = {}
    parts = []
    in_workflows = True
    with open(infile, "r", encoding="utf-8") as f:
        for line in f:
            if len(line.rstrip()) == 0:
                in_workflows = False
                continue
            if in_workflows:
                name, rules = parse_workflow(line)
                workflows[name] = rules
            else:
                # {x=787,m=2655,a=1222,s=2876}
                part_properties = line.rstrip()[1:-1].split(",")
                parts.append({
                    prop: int(value) for prop, value in [p.split("=") for p in part_properties]
                })
    return workflows, parts


def solve(input):
    def apply_condition(condition, part):
        if condition == "true":
            return True
        
        property, comparison, value = condition
        if comparison == ">":
            return part[property] > value
        return part[property] < value
    
    result = 0
    workflows, parts = input
    for part in parts:
        step = "in"
        while step not in ["A", "R"]:
            workflow = workflows[step]
            for rule in workflow:
                if apply_condition(rule["condition"], part):
                    step = rule["next"]
                    break
        if step == "A":
            result += sum(part.values())
    return result

def solve2(input):
    def num_combinations(path):
        def compare(a, comp, b):
            if comp == "<":
                return a < b
            if comp == ">":
                return a > b
            if comp == "<=":
                return a <= b
            if comp == ">=":
                return a >= b
            assert False 

        if "false" in path:
            return 0
        
        properties = {
            "x": set(range(1,4001)),
            "m": set(range(1,4001)),
            "a": set(range(1,4001)),
            "s": set(range(1,4001))
        }
        for condition in path:
            if condition == "true":
                continue
            prop, comp, val = condition
            properties[prop] = set(v for v in properties[prop] if compare(v, comp, val))
        return len(properties["x"]) * len(properties["m"]) * len(properties["a"]) * len(properties["s"])



    workflows, _ = input
    dp = {}
    def solve_rec(step, idx):
        def invert(condition):
            if condition == "true":
                return "false"
            prop, comp, val = condition
            new_comp = ">=" if comp == "<" else "<="
            return (prop, new_comp, val)
            

        if idx >= len(workflows[step]):
            return [["false"]]
        
        if (step, idx) not in dp:
            rule = workflows[step][idx]

            condition = rule["condition"]
            paths = []
            if rule["next"] == "A":
                paths.append([condition])
                for rec_path in solve_rec(step, idx+1):
                    paths.append([invert(condition)] + rec_path)
            elif rule["next"] == "R":
                for rec_path in solve_rec(step, idx+1):
                    paths.append([invert(condition)] + rec_path)
            else:
                for rec_path in solve_rec(rule["next"], 0):
                    paths.append([condition] + rec_path)
                for rec_path in solve_rec(step, idx+1):
                    paths.append([invert(condition)] + rec_path)

            dp[(step,idx)] = paths
    
        return dp[(step, idx)]
    
    
    winning = solve_rec("in", 0)
    sum = 0
    for path in winning:
        inc = num_combinations(path)
        sum += inc
    return sum



@click.command()
@click.argument("infile")
def main(infile):
    input = read(infile)
    sol = solve2(input)
    print(sol)
    
if __name__ == "__main__":
    main()