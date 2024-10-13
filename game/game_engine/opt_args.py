from abc import ABC, abstractmethod
from typing import Any, Dict


class IOptArgs(ABC):
    def __init__(self, kwargs: Dict[str, Any]) -> None:
        super().__init__()
        self.kwargs:Dict[str,Any] = kwargs
        
    @abstractmethod
    def get_kwargs(self) -> Dict[str,Any]:
        pass


class OptArgs(IOptArgs):
    def __init__(self, kwargs: Dict[str, Any]) -> None:
        super().__init__(kwargs)
        
    def get_kwargs(self) -> Dict[str,Any]:
        return self.kwargs
    