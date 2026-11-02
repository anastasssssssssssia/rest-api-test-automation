def double(value: int) -> int:
    return value * 2


class UserValidator:
    @staticmethod
    def is_valid_id(user_id: int) -> bool:
        return isinstance(user_id, int) and not isinstance(user_id, bool) and user_id > 0

    @staticmethod
    def is_valid_email(email: str) -> bool:
        if not isinstance(email, str) or "@" not in email:
            return False
        name, domain = email.split("@", 1)
        has_dot = "." in domain
        dot_at_edge = domain.startswith(".") or domain.endswith(".")
        return bool(name) and has_dot and not dot_at_edge
