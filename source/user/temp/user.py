from dataclasses import dataclass

@dataclass (frozen=True)
class UserDto:
    id_user: int = None,
    name: str = "",
    email: str = "",
    login: str = "",
    password: str = "",
    is_mod: bool = False     