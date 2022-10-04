import random

from tykes.farkle import parse_dice



def test_straight():
    """A straight is worth 1000 points."""
    assert parse_dice([1, 2, 3, 4, 5, 6]).value == 1000


def test_three_pairs():
    """Three pairs should always be worth 750 points."""
    sides = list(range(1, 7))
    random.shuffle(sides)

    # build three pairs
    dice = []
    for _ in range(3):
        dice.append(sides.pop(0))
        dice.append(dice[-1])


    assert parse_dice(dice).value == 750
    assert parse_dice([6, 6, 1, 1, 4, 4]).value == 750
    assert parse_dice([1, 1, 3, 3, 5, 5]).value == 750
    assert parse_dice([1, 1, 5, 5, 2, 2]).value == 750


def test_four_of_a_kind():
    """If four of a kind is enabled, it should be double the value of three of a kind."""
    for side in range(1, 7):
        assert parse_dice([side, side, side, side]).value == parse_dice([side, side, side]).value * 2


def test_three_of_a_kind():
    """Three of a kind is worth the dice face * 100, except 1s, which are 1000."""
    assert parse_dice([1, 1, 1]).value == 1000
    for side in range(2, 7):
        assert parse_dice([side, side, side]).value == side * 100


def test_pair_of_ones():
    """Ensure 2 ones present are always worth 200."""
    assert parse_dice([1, 1, 2, 2, 3, 4]).value == 200
    assert parse_dice([1, 1, 2, 3, 3, 4]).value == 200
    assert parse_dice([1, 1, 2, 3, 4, 4]).value == 200
    assert parse_dice([1, 1, 2, 3, 4, 6]).value == 200
    assert parse_dice([1, 1, 3, 4, 6, 6]).value == 200


def test_one():
    """Ensure one 1 is only worth 100."""
    useless = [2, 3, 4, 6]
    random.shuffle(useless)

    dice = [1]
    dice.extend(useless)
    dice.append(dice[-1])
    dice.sort()

    assert parse_dice(dice).value == 100


def test_pair_of_fives():
    """Ensure 2 fives present are always worth 100."""
    assert parse_dice([5, 5, 2, 2, 3, 4]).value == 100
    assert parse_dice([5, 5, 2, 3, 3, 4]).value == 100
    assert parse_dice([5, 5, 2, 3, 4, 4]).value == 100
    assert parse_dice([5, 5, 2, 3, 4, 6]).value == 100
    assert parse_dice([5, 5, 3, 4, 6, 6]).value == 100


def test_one():
    """Ensure one 5 is only worth 50."""
    useless = [2, 3, 4, 6]
    random.shuffle(useless)

    dice = [5]
    dice.extend(useless)
    dice.append(dice[-1])
    dice.sort()

    assert parse_dice(dice).value == 50


def test_no_remainder():
    """Ensure all dice are consumed."""
    assert not parse_dice([1, 2, 3, 4, 5, 6]).remainder
    assert not parse_dice([1, 1]).remainder
    assert not parse_dice([5]).remainder
