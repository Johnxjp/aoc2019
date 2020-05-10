from helper import load


def calculate_fuel(mass: int) -> int:
    return (mass // 3) - 2


def main():
    modules = load("data/d1.txt")
    return sum(calculate_fuel(module_mass) for module_mass in modules)


if __name__ == "__main__":
    print(main())
