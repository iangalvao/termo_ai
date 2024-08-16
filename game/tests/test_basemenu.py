import pytest
from unittest.mock import Mock

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


def test_set_action_new_action():
    menu = BaseMenu()
    action = Mock(spec=Action)
    menu.set_action(action, "start_game")

    assert menu.actions_ids == ["start_game"]
    assert menu.actions["start_game"] == action


def test_set_action_override():
    menu = BaseMenu()
    action1 = Mock(spec=Action)
    action2 = Mock(spec=Action)
    menu.set_action(action1, "start_game")
    menu.set_action(action2, "start_game")

    assert len(menu.actions_ids) == 1
    assert menu.actions["start_game"] == action2


def test_set_action_invalid_id_empty_string():
    menu = BaseMenu()
    action = Mock(spec=Action)

    with pytest.raises(ValueError, match="Action ID must be a non-empty string."):
        menu.set_action(action, "")


def test_set_action_invalid_id_none():
    menu = BaseMenu()
    action = Mock(spec=Action)

    with pytest.raises(ValueError, match="Action ID must be a non-empty string."):
        menu.set_action(action, None)
