from typing import List
import pytest
import unittest
from unittest.mock import Mock

from game.game_states.action import Action
from game.game_states.end_match_menu import EndMatchMenu, EndMatchState, MatchResult
from game.game_states.igame_context import IGameContext
from game.model.challenge import IChallenge
from game.model.match import IMatch
from game.viewer.imenu_presenter import IMenuPresenter


@pytest.fixture
def dummy_context():
    class DummyGameContext(IGameContext):
        def change_state(self, state_id: str, **kwargs) -> None:
            pass

        def handle_input(self, input) -> None:
            pass  # Implementation not needed for this test

    return DummyGameContext()


@pytest.fixture
def results():
    return MatchResult(won=True, n_attempts=5, correct_words=["abcde", "fghij"])


@pytest.fixture
def expected_menu(dummy_context, results):
    m = EndMatchMenu(results)

    m.actions = {
        "retry": Action(
            dummy_context.change_state, **{"state_id": "play_state", "n_challenges": 2}
        ),
        "main menu": Action(
            dummy_context.change_state, **{"state_id": "main_menu_state"}
        ),
        "quit": Action(dummy_context.change_state, **{"state_id": "quit_state"}),
        "back": Action(dummy_context.change_state, **{"state_id": "play_state"}),
    }
    m.actions_ids = ["retry", "main menu", "quit", "back"]
    return m


@pytest.fixture
def dummy_match(results):
    class DummyMatch(IMatch):
        def won(self) -> bool:
            pass

        def get_n_attempts(self) -> int:
            pass

        def get_results(self):
            return results

        def get_challenges(self) -> List[IChallenge]:
            pass

        def get_words(self) -> List[str]:
            pass

        def delete_letter(self, pos: int) -> None:
            pass

        def input_letter(self) -> str:
            pass

        def move_cursor_left(self) -> None:
            pass

        def move_cursor_right(self) -> None:
            pass

        def submit_guess(self) -> str:
            pass

        def check_valid_word(self, word: str) -> bool:
            pass

        def update(self, guess: str) -> None:
            pass

    dummy_match = DummyMatch(challenges=None, accepted_words=None)
    dummy_match.n_challenges = 2
    return dummy_match


def test_on_enter_initializes_menu(expected_menu, dummy_context, dummy_match, results):
    # Create mocks for the context and presenter
    presenter = Mock(spec=IMenuPresenter)

    # Initialize the MainMenuState
    state = EndMatchState(presenter=presenter)

    # Call on_enter and verify the menu was created with correct actions
    state.on_enter(dummy_context, match=dummy_match)

    presenter.display_menu.assert_called_with(state.menu)
    assert (
        state.menu == expected_menu
    ), f"\nSTATE.MENU:\n {state.menu}\nEXPECTED MENU:\n{expected_menu}"
    # Verify that the menu was displayed
