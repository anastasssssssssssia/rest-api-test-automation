def double(value: int) -> int:
    return value * 2


class UserValidator:
    @staticmethod
    def is_valid_id(user_id: int) -> bool:
        return isinstance(user_id, int) and not isinstance(user_id, bool) and user_id > 0

    @staticmethod
    def is_valid_email(email: str) -> bool:
        if not isinstance(email, str):
            return False

        if email.count("@") != 1:
            return False

        if any(char.isspace() for char in email):
            return False

        name, domain = email.split("@")
        return (
            bool(name)
            and "." in domain
            and not domain.startswith(".")
            and not domain.endswith(".")
        )
