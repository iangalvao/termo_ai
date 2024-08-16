import pytest
import unittest
from unittest.mock import Mock

from game.controller.end_game_controller import (
    Action,
    IGameContext,
    MainMenu,
    MainMenuState,
    IMenuPresenter,
)


@pytest.fixture
def dummy_context():
    class DummyGameContext(IGameContext):
        def change_state(self, state_id: str, **kwargs) -> None:
            pass

        def handle_input(self, input) -> None:
            pass  # Implementation not needed for this test

    return DummyGameContext()


@pytest.fixture
def expected_menu(dummy_context):
    m = MainMenu()
    m.actions = {
        "quick match": Action(
            dummy_context.change_state, **{"state_id": "play_state", "n_challenges": 1}
        ),
        "new match": Action(dummy_context.change_state, **{"state_id": "match_config"}),
        "quit": Action(dummy_context.change_state, **{"state_id": "quit_state"}),
    }
    m.actions_ids = ["quick match", "new match", "quit"]
    return m


def test_on_enter_initializes_menu(expected_menu, dummy_context):
    # Create mocks for the context and presenter
    presenter = Mock(spec=IMenuPresenter)

    # Initialize the MainMenuState
    state = MainMenuState(presenter=presenter)

    # Call on_enter and verify the menu was created with correct actions
    state.on_enter(dummy_context)

    presenter.display_menu.assert_called_with(state.menu)
    assert (
        state.menu == expected_menu
    ), f"\nSTATE.MENU:\n {state.menu}\nEXPECTED MENU:\n{expected_menu}"
    # Verify that the menu was displayed
