from abc import ABC, abstractmethod
from functools import wraps
import inspect
from typing import Tuple
from typing_extensions import override
from game.game_engine.igame_context import IGameContext
from game.game_engine.menus.menu import IMenu
from game.game_engine.presenters.imenu_presenter import IMenuPresenter

def expandable_args(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        # Get the class of the method being decorated
        #cls = args[0].__class__

        sig = inspect.signature(method)
        for name, param in kwargs.items():
          print(f"({name}, {param})")
          if name not in sig.parameters.keys():
                print("THIS ONE IS EXTRA: ", name)  
                raise TypeError(f"{method.__name__} does not accept **kwargs. All arguments must be explicitly defined.")

        print("PRINT kwargs =", kwargs)
        # Check if the class is abstract]
        # Check if kwargs is not empty
        # Call the original method
        return method(*args, **kwargs)
    
    return wrapper


class DummyPresenter(IMenuPresenter):
    def display_menu(self, menu: IMenu | None = None) -> None:
        pass
    def clear_menu(self) -> None:
        pass
    def message(self, message: str, pos: Tuple[int, int]) -> None:
        pass
    
    
class DummyContext(IGameContext):
    def handle_input(self, input) -> None:
        pass
    def change_state(self, state_id: str, **kwargs) -> None:
        pass
   

@expandable_args
def foo(x: int = 0, **kwargs):
    return x


# This will raise a TypeError because kwargs is not empty:
class IFoo(ABC):
    @abstractmethod
    def f(self):
        pass
    @abstractmethod
    @expandable_args
    def some_method(self, **kwargs):
        pass


class Foo(IFoo):
    @override
    def f(self):
        pass
   # @mydecorator  # This will raise a TypeError
    @override
    @expandable_args
    def some_method(self, **kwargs):
        print("FOO")


foo_object = Foo()
foo_object.some_method()  # This would raise an error due to the decorator being applied in a concrete class
