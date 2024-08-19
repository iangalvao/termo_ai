from typing import Any, Callable


class Action:
    def __init__(self, f: Callable[[], None], **kwargs) -> None:
        self.func = f
        self.fixed_args = kwargs

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        combined_args = {**self.fixed_args, **kwds}
        return self.func(*args, **combined_args)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Action):
            return self.func == other.func and self.fixed_args == other.fixed_args
        return False

    def __str__(self) -> str:
        return f"Action(func={self.func.__name__}, fixed_args={self.fixed_args})"

    def __repr__(self) -> str:
        return str(self)
