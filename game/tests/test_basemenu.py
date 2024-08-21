import pytest
from unittest.mock import Mock

from game.game_states.action import Action as GameAction
from game.game_states.base_menu import BaseMenu


def dummy_func(a, b):
    return a + b


def test_base_menu_equality():
    menu1 = BaseMenu()
    menu2 = BaseMenu()

    action1 = GameAction(dummy_func, a=1)
    action2 = GameAction(dummy_func, a=2)

    menu1.set_action(action1, "action1")
    menu1.set_action(action2, "action2")

    menu2.set_action(action1, "action1")
    menu2.set_action(action2, "action2")

    assert menu1 == menu2

    # Test that changing the focus results in inequality
    menu2.move_focus(1)
    assert menu1 != menu2

    # Test that removing an action results in inequality
    menu2.unregister_action("action1")
    assert menu1 != menu2


def test_set_action_new_action():
    menu = BaseMenu()
    action = Mock(spec=GameAction)
    menu.set_action(action, "start_game")

    assert menu.actions_ids == ["start_game"]
    assert menu.actions["start_game"] == action


def test_set_action_override():
    menu = BaseMenu()
    action1 = Mock(spec=GameAction)
    action2 = Mock(spec=GameAction)
    menu.set_action(action1, "start_game")
    menu.set_action(action2, "start_game")

    assert len(menu.actions_ids) == 1
    assert menu.actions["start_game"] == action2


def test_set_action_invalid_id_empty_string():
    menu = BaseMenu()
    action = Mock(spec=GameAction)

    with pytest.raises(ValueError, match="Action ID must be a non-empty string."):
        menu.set_action(action, "")


def test_set_action_invalid_id_none():
    menu = BaseMenu()
    action = Mock(spec=GameAction)

    with pytest.raises(ValueError, match="Action ID must be a non-empty string."):
        menu.set_action(action, None)


@pytest.fixture
def dummy_action():
    def dummy():
        return

    return GameAction(dummy)


@pytest.fixture
def action_mock_pair():
    mock = Mock()
    return (GameAction(mock), mock)


def test_unregister_action(dummy_action):
    menu = BaseMenu()
    menu.set_action(dummy_action, "action_1")
    menu.set_action(dummy_action, "action_2")

    # Test unregistering an existing action
    menu.unregister_action("action_1")
    assert "action_1" not in menu.actions
    assert "action_1" not in menu.actions_ids

    # Test unregistering an action that doesn't exist
    with pytest.raises(KeyError):
        menu.unregister_action("non_existent_action")


def test_unregister_action_twice_same_id_should_return_key_error(dummy_action):
    menu = BaseMenu()
    menu.set_action(dummy_action, "action_1")
    menu.set_action(dummy_action, "action_2")

    # Test unregistering an existing action
    menu.unregister_action("action_1")
    assert "action_1" not in menu.actions
    assert "action_1" not in menu.actions_ids

    # Test unregistering an action that doesn't exist
    with pytest.raises(KeyError):
        menu.unregister_action("action_1")


def test_move_focus(dummy_action):
    menu = BaseMenu()
    menu.set_action(dummy_action, "action_1")
    menu.set_action(dummy_action, "action_2")
    menu.set_action(dummy_action, "action_3")

    # Initial focus should be 0
    assert menu.focus == 0

    # Test moving focus down (positive direction)
    menu.move_focus(1)
    assert menu.focus == 1

    # Test moving focus up (negative direction)
    menu.move_focus(-1)
    assert menu.focus == 0

    # Test moving focus beyond the first action (negative direction)
    menu.move_focus(-1)
    assert menu.focus == 0  # Should not change, as it's already at the start

    # Test moving focus beyond the last action (positive direction)
    menu.move_focus(3)
    assert menu.focus == 0  # Should not change, as 0 + 3 = 3 is out of bounds

    # Test moving focus to the last valid action
    menu.move_focus(2)
    assert menu.focus == 2


def test_call_action_on_focus_with_empty_actions():
    menu = BaseMenu()

    with pytest.raises(IndexError):
        menu.call_action_on_focus()  # Should raise an IndexError when actions are empty


def test_call_action_on_focus():
    menu = BaseMenu()

    action_mock = Mock()
    wrapped_action = GameAction(action_mock)
    menu.set_action(wrapped_action, "action_1")

    menu.call_action_on_focus()

    action_mock.assert_called_once()

    # Test calling action after moving focus
    action_mock_2 = Mock()
    wrapped_action_2 = GameAction(action_mock_2)
    menu.set_action(wrapped_action_2, "action_2")
    menu.move_focus(1)

    menu.call_action_on_focus()

    action_mock_2.assert_called_once()
    action_mock.assert_called_once()  # Should still be called only once


def test_end_menu(action_mock_pair):
    menu = BaseMenu()
    menu.set_action(action_mock_pair[0], "back")

    menu.end_menu()

    action_mock_pair[1].assert_called_once()
