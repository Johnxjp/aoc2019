def is_valid_number(num: int) -> bool:
    has_adjacent_pairs = False
    prev_char = str(num)[0]
    for char in str(num)[1:]:
        if char == prev_char:
            has_adjacent_pairs = True

        if char < prev_char:
            return False

        prev_char = char

    return has_adjacent_pairs


def count_valid(low: int, high: int) -> int:
    count = 0
    for num in range(low, high + 1):
        count += is_valid_number(num)

    return count


def main():
    low, high = 171309, 643603
    return count_valid(low, high)


if __name__ == "__main__":
    print(main())
