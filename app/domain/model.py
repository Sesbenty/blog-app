from dataclasses import dataclass


@dataclass
class User:
    email: str
    first_name: str
    last_name: str
    password: str

    id: int = None

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"
