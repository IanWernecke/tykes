from copy import deepcopy
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Combination:
    name: str  # triple, straight, three-of-a-kind, four-of-a-kind
    dice: list
    value: int


@dataclass
class ParsedDice:
    combos: List[Combination]
    remainder: List[int]
    value: int


def dice_count(dice: List[int]) -> Dict[int, int]:
    """Count the dice inside of a given list, no zeroes listed."""
    result = dict()
    for die in dice:
        if die not in result:
            result[die] = dice.count(die)
    return result


def dice_contains(super_dice: List[int], sub_dice: List[int]) -> bool:
    """Check whether a superset of dice contains a subset."""
    for side in range(1, 7):
        if sub_dice.count(side) > super_dice.count(side):
            return False
    return True


def parse_dice(dice: List[int]) -> ParsedDice:
    """Parse the combinations, remainder, and value of the given dice."""
    combos = []
    remainder = deepcopy(dice)
    value = 0

    def _check(_name: str, _dice: List[int], _value: int) -> bool:
        """Determine if a combination is present in the given dice."""
        nonlocal combos, remainder, value
        if not dice_contains(remainder, _dice):
            return False
        combos.append(Combination(name=_name, dice=_dice, value=_value))
        for _die in _dice:
            remainder.pop(remainder.index(_die))
        value += _value
        return True

    # straight
    if _check("straight", [1, 2, 3, 4, 5, 6], 1000):
        return ParsedDice(combos=combos, remainder=remainder, value=value)

    # three pairs
    # WARNING: ensure dice given are a deepcopy and reflect the actual remaining
    counted = dice_count(remainder)
    if len(counted.keys()) == 3 and all(counted[side] == 2 for side in counted):
        _check("three_pairs", _dice=deepcopy(remainder), _value=750)

    # oak == one of a kind
    # if any of the counted dice had more than two, the above three pair check
    #   would have failed and this would be possible
    if any(value >= 3 for _, value in counted.items()):

        # six oak
        _check("six_1s", [1] * 6, 1000 * 8)
        for side in range(2, 7):
            _check("six_{side}s", [side] * 6, side * 100 * 8)

        # five oak
        _check("five_1s", [1] * 5, 1000 * 4)
        for side in range(2, 7):
            _check("five_{side}s", [side] * 5, side * 100 * 4)

        # four oak
        _check("four_1s", [1] * 4, 1000 * 2)
        for side in range(2, 7):
            _check("four_{side}s", [side] * 4, side * 100 * 2)

        # three oak
        _check("three_1s", [1] * 3, 1000)
        for side in range(2, 7):
            _check("three_{side}s", [side] * 3, side * 100)

    if not remainder:
        return ParsedDice(combos=combos, remainder=remainder, value=value)

    # ones and fives
    _check("one", [1], 100)
    _check("one", [1], 100)
    _check("five", [5], 50)
    _check("five", [5], 50)

    return ParsedDice(combos=combos, remainder=remainder, value=value)
