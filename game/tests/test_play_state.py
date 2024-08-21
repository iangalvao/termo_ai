import pytest
import unittest
from unittest.mock import Mock

from game.game_states.igame_context import IGameContext
from game.game_states.play_state import IMatchController, PlayState
from game.viewer.game_display import IGameDisplay


@pytest.fixture
def dummy_context():
    class DummyGameContext(IGameContext):
        def change_state(self, state_id: str, **kwargs) -> None:
            pass

        def handle_input(self, input) -> None:
            pass  # Implementation not needed for this test

    return DummyGameContext()


@pytest.fixture
def mock_presenter():
    presenter = Mock(spec=IGameDisplay)
    return presenter


@pytest.fixture
def match_controller():
    class DummyMatchController(IMatchController):
        def submit_guess(self, guess: str) -> None:
            pass

        def new_match(self, n_challenges: int) -> None:
            pass

    return DummyMatchController()


@pytest.fixture
def play_state(mock_presenter, match_controller):
    return PlayState(mock_presenter, match_controller)


def test_move_cursor_right(play_state, dummy_context):
    # Call on_enter and verify the menu was created with correct actions
    play_state.move_cursor_right()

    assert play_state.cursor == 1
