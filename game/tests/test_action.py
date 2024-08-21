import pytest

from game.game_states.action import Action


def dummy_func(a, b):
    return a + b


def test_action_equality():
    action1 = Action(dummy_func, a=1)
    action2 = Action(dummy_func, a=1)

    assert action1 == action2

    action3 = Action(dummy_func, a=2)
    assert action1 != action3
