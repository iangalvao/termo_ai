import pytest
from unittest.mock import Mock

from game.controller.match_controller import MatchStartParams
from game.game_engine.igame_context import IGameContext
from game.game_states.play_state import IMatchController, PlayState
from game.model.imatch import IMatch
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

        #def new_match(self, n_challenges: int) -> None:
         #   pass

        def new_match(self, match_params: MatchStartParams) -> None:
            return None
        def get_match(self) -> IMatch | None:
            return None
        def get_results(self):
            return None
        def won(self) -> bool:
            return False
        
    return DummyMatchController()


@pytest.fixture
def play_state(mock_presenter, match_controller):
    return PlayState(mock_presenter, match_controller)

