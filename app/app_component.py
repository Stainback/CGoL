from abc import ABC, abstractmethod


class AppComponent(ABC):
    @abstractmethod
    def draw(self):
        pass
