day1_input = [int(x) for x in open("day1_input", "r").read().splitlines()]

depth_pairs = list(zip(day1_input, day1_input[1:] + []))

diffs = [depth[1] - depth[0] for depth in depth_pairs if depth[0] - depth[1] < 0]

print(len(diffs))