
from dataclasses import dataclass


@dataclass
class Measurement:
    x: int
    y: int
    z: int

    @property
    def sum(self):
        return self.x + self.y + self.z


day1_input = [int(depth_str) for depth_str in open("day1_input", "r").read().splitlines()]

depth_triplets = list(zip(day1_input, day1_input[1:], day1_input[2:]))

measurements = [Measurement(x, y, z) for x, y, z in depth_triplets]

zipped_measurements = list(zip(measurements, measurements[1:]))

measurement_diffs = [
    measurement1.sum - measurement2.sum
    for measurement1, measurement2  in zipped_measurements
    if measurement1.sum - measurement2.sum < 0
]

print(len(measurement_diffs))