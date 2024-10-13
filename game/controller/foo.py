'''
Hi! Here's a code that exemplifies a problem i found with vscode python extension error marks when used with typing, interfaces and lists:
'''

from abc import ABC, abstractmethod
from typing import List

# Class to be passed as arg in bar classes constructors.

# Interface
class IFoo(ABC):
    def __init__(self) -> None:
        super().__init__()
        
# Implementation
class Foo(IFoo):
    def __init__(self) -> None:
        super().__init__()



# Class that receives a single IFoo object in the contructor

# Interface
class IBar(ABC):
    def __init__(self, foo: IFoo) -> None:
        super().__init__()

    @abstractmethod
    def f(self) -> IFoo:
        pass

# Impelentation
class Bar(IBar):
    def __init__(self, foo: IFoo) -> None:
        super().__init__(foo)
        self.foo = foo
    def f(self) -> IFoo:
        return self.foo

# Everithing is OK here
foo = Foo()
bar = Bar(foo)

# Class that uses a List of Foos in the constructor

# Interface
class IListBar(ABC):
    def __init__(self, foos: List[IFoo]) -> None:
        super().__init__()

    @abstractmethod
    def f(self) -> List[IFoo]:
        pass

# Implementation
class ListBar(IListBar):
    def __init__(self, foos: List[IFoo]) -> None:
        super().__init__(foos)
        self.foos = foos
    def f(self) -> List[IFoo]:
        return self.foos


foos: List[IFoo] = [Foo(), Foo(), Foo()]
list_bar = ListBar(foos) # In this line is the VSCode python extension is marking the error

'''
The error is:
    Argument 1 to "ListBar" has incompatible type "list[Foo]"; expected "list[IFoo]"Mypyarg-type

When constructor receives the interface directly, i can call with an object of a class that implements that interface (have as its superclass).
However, when it receives a list of interfaces as arguments, it can be initializated with objects that implements that interface.
Is this the expected behavior or a issue?
'''