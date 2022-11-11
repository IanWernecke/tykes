from tykes.utils import neighbors


def test_neighbors():

    # n.
    # @n
    n = list(neighbors(0, 0, 2, 2))

    assert len(n) == 2
    assert (0, 1) in n
    assert (1, 0) in n

    # n@
    # .n
    n = list(neighbors(1, 1, 2, 2))

    assert len(n) == 2
    assert (0, 1) in n
    assert (1, 0) in n

    # n..
    # @n.
    # n..
    n = list(neighbors(0, 1, 3, 3))

    assert len(n) == 3
    assert (0, 0) in n
    assert (1, 1) in n
    assert (0, 2) in n


    # .n.
    # n@n.
    # .n.
    n = list(neighbors(1, 1, 3, 3))

    assert len(n) == 4
    assert (1, 2) in n  # top
    assert (2, 1) in n  # right
    assert (1, 0) in n  # bottom
    assert (0, 1) in n  # left
