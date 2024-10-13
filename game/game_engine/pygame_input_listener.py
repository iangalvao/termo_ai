from game.game_engine.controllercore import IInputListener


class PygameInputListener(IInputListener):
    def __init__(self) -> None:
        super().__init__()
