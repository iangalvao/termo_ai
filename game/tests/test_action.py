from game.controller.end_game_controller import Action
import pytest


def dummy_func(a, b):
    return a + b


def test_action_equality():
    action1 = Action(dummy_func, a=1)
    action2 = Action(dummy_func, a=1)

    assert action1 == action2

    action3 = Action(dummy_func, a=2)
    assert action1 != action3
