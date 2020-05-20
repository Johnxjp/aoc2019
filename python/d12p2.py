from dataclasses import dataclass
from typing import Sequence
from math import gcd
from functools import reduce


def lcm(denominators):
    return reduce(lambda a, b: a * b // gcd(a, b), denominators)


@dataclass
class Vector3D:
    x: int = 0
    y: int = 0
    z: int = 0

    def __add__(self, other: "Vector3D") -> "Vector3D":
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)


@dataclass
class Moon:
    name: str
    pos: Vector3D
    vel: Vector3D

    def update_position(self) -> None:
        self.pos = self.pos + self.vel

    def pe(self) -> int:
        """Potential energy"""
        pos = self.pos
        return abs(pos.x) + abs(pos.y) + abs(pos.z)

    def ke(self) -> int:
        """Kinetic energy"""
        vel = self.vel
        return abs(vel.x) + abs(vel.y) + abs(vel.z)

    def total_energy(self) -> int:
        return self.pe() * self.ke()


def gravitational_effect(moon: Moon, other_moons: Sequence[Moon]) -> Vector3D:
    """"Returns how velocity is impacted by other moons"""
    deltas = [0, 0, 0]
    for om in other_moons:
        for i, attr in enumerate(["x", "y", "z"]):
            if getattr(moon.pos, attr) < getattr(om.pos, attr):
                deltas[i] += 1

            if getattr(moon.pos, attr) > getattr(om.pos, attr):
                deltas[i] -= 1

    return Vector3D(deltas[0], deltas[1], deltas[2])


def representation(moons: Sequence[Moon], attr: str) -> str:
    string = ""
    for moon in moons:
        for num in [getattr(moon.pos, attr), getattr(moon.vel, attr)]:
            string += str(num)

    return string


def main():
    moons = [
        Moon("Io", pos=Vector3D(-19, -4, 2), vel=Vector3D()),
        Moon("Europa", pos=Vector3D(-9, 8, -16), vel=Vector3D()),
        Moon("Ganymede", pos=Vector3D(-4, 5, -11), vel=Vector3D()),
        Moon("Callisto", pos=Vector3D(1, 9, -13), vel=Vector3D()),
    ]
    cycles = {"x": 0, "y": 0, "z": 0}
    step = 0
    history = {
        "x": set(representation(moons, "x")),
        "y": set(representation(moons, "y")),
        "z": set(representation(moons, "z")),
    }
    while not all(cycles.values()):
        # calculate gravity
        pos_change = [0] * len(moons)
        for i in range(len(moons)):
            pos_change[i] = gravitational_effect(moons[i], moons[:i] + moons[i + 1 :])

        # Apply gravity
        for moon, delta in zip(moons, pos_change):
            moon.vel += delta

        # update positions
        for moon in moons:
            moon.update_position()

        for attr in ["x", "y", "z"]:
            if not cycles[attr]:
                new_rep = representation(moons, attr)
                if new_rep in history[attr]:
                    print(attr, step)
                    cycles[attr] = step
                else:
                    history[attr].add(new_rep)

        step += 1

    return lcm(cycles.values())


if __name__ == "__main__":
    print(main())
