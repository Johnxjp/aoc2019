def main():
    with open("data/d8.txt") as f:
        data = f.read().strip()

    image_w = 25
    image_h = 6
    n_pixels = image_w * image_h
    layers = [data[i : i + n_pixels] for i in range(0, len(data), n_pixels)]
    min_zeros = len(layers[0]) + 1
    output = 0
    for layer_idx, layer in enumerate(layers):
        if (zero_count := layer.count("0")) < min_zeros:
            one_count, two_count = layer.count("1"), layer.count("2")
            output = one_count * two_count
            min_zeros = zero_count

    return output


if __name__ == "__main__":
    print(main())
