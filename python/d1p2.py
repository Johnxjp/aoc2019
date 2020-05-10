from helper import load


def calculate_fuel_acc(mass: int) -> int:
    total_fuel = 0
    while (mass := (mass // 3) - 2) > 0:
        total_fuel += mass

    return total_fuel


def main():
    modules = load("data/d1.txt")
    return sum(calculate_fuel_acc(module_mass) for module_mass in modules)


if __name__ == "__main__":
    print(main())
