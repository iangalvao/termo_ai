import pytest

from game.controller.end_game_controller import Action, BaseMenu


def dummy_func(a, b):
    return a + b


def test_base_menu_equality():
    menu1 = BaseMenu()
    menu2 = BaseMenu()

    action1 = Action(dummy_func, a=1)
    action2 = Action(dummy_func, a=2)

    menu1.set_action(action1, "action1")
    menu1.set_action(action2, "action2")

    menu2.set_action(action1, "action1")
    menu2.set_action(action2, "action2")

    assert menu1 == menu2

    # Test that changing the focus results in inequality
    menu2.move_focus(1)
    assert menu1 != menu2

    # Test that removing an action results in inequality
    menu2.remove_action_hook("action1")
    assert menu1 != menu2
