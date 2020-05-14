from typing import Sequence


def load(file: str) -> Sequence[int]:
    """Loads a list of numbers each on a new line"""
    data = []
    with open(file) as f:
        for line in f:
            data.append(int(line.strip()))
    return data


def loadv2(file: str) -> Sequence[int]:
    """Loads a list of numbers separated by a comma"""
    data = []
    with open(file) as f:
        data = f.read().strip()
        data = list(map(int, data.split(",")))
    return data


def loadv3(file: str) -> Sequence[Sequence[str]]:
    """Loads a list of strings separated by a comma"""
    data = []
    with open(file) as f:
        for line in f:
            path = line.strip().split(",")
            data.append(path)
    return data


def loadv4(file: str) -> Sequence[int]:
    """Loads a list of strings each on a new line"""
    data = []
    with open(file) as f:
        for line in f:
            data.append(line.strip())
    return data