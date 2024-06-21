from abc import ABC, abstractmethod

from musync.entity import User


class Session(ABC):

    @property
    @abstractmethod
    def user(self) -> User:
        pass

    @abstractmethod
    def check_login(self) -> bool:
        pass
