from dataclasses import dataclass


@dataclass
class User:
    id: int
    first_name: str
    last_name: str

    @property
    def full_name(self) -> str:
        parts = [self.first_name.strip(), self.last_name.strip()]
        return " ".join(part for part in parts if part)
