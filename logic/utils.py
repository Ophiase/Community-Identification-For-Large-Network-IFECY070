from typing import Generator, Tuple


def _external_pair(set_size: int) -> Generator[Tuple[int, int], None, None]:
    for x in range(set_size):
        for y in range(1 + x, set_size):
            yield x, y


def _pair(set_size: int) -> Generator[Tuple[int, int], None, None]:
    for x in range(set_size):
        for y in range(x, set_size):
            yield x, y


def _cartesian_product(X, Y) -> Generator[Tuple[int, int], None, None]:
    for x in X:
        for y in Y:
            yield x, y
