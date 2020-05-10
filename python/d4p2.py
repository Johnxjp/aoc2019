def is_valid_number(num: int) -> bool:
    has_single_pair = False
    count = 1
    prev_char = str(num)[0]
    for char in str(num)[1:]:
        if char == prev_char:
            count += 1
        
        if char < prev_char:
            return False
        
        if char != prev_char:
            if count == 2:
                has_single_pair = True
            count = 1

        prev_char = char
    else:
        if count == 2:
            has_single_pair = True

    return has_single_pair


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
    print(is_valid_number(455))