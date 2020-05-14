def main():
    with open("data/d8.txt") as f:
        data = f.read().strip()

    image_w, image_h = 25, 6
    n_pixels = image_w * image_h
    image = ""
    for pixel_id in range(n_pixels):
        while data[pixel_id] == "2":
            pixel_id += n_pixels
        else:
            image += data[pixel_id]

    image = [image[i : i + image_w] for i in range(0, len(image), image_w)]
    for row in image:
        for c in row:
            print(" " if c == "0" else "X", end="")
        print()


if __name__ == "__main__":
    main()

