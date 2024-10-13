from abc import ABC, abstractmethod
import functools
import inspect
from typing_extensions import override

def mydecorator(method):

    # Get the class in which the method was defined
    frame = inspect.currentframe().f_back
    class_defining_method = frame.f_locals.get('__qualname__', '').split('.')[0]

    # Get the class object by name
    defined_on_abstract = True
    #if not inspect.isabstract(class_defining_method):
    if not isinstance(class_defining_method, ABC) or not hasattr(class_defining_method, '__abstractmethods__'):
        defined_on_abstract = False
        raise TypeError(f"Decorator 'mydecorator' cannot be applied to a method in a concrete class '{class_defining_method}'.")
    
    @functools.wraps(method)
    def wrapper(*args, defined_on_abstract = defined_on_abstract, **kwargs):
        print("Entering wrapper")
        cls = args[0].__class__
        if not defined_on_abstract:
            raise TypeError(f"Decorator 'mydecorator' cannot be applied to a method in a concrete class '{cls.__name__}'.")
        return method(*args, **kwargs)

    return wrapper


class IFoo(ABC):
    @abstractmethod
    def f(self):
        pass
    @abstractmethod
    @mydecorator
    def some_method(self):
        pass


class Foo(IFoo):
    @override
    def f(self):
        pass
   # @mydecorator  # This will raise a TypeError
    @override
    def some_method(self):
        print("FOO")


foo = Foo()
foo.some_method()  # This would raise an error due to the decorator being applied in a concrete class
