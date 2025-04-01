import re


def validate_email(email: str) -> str:
    if re.match(r"^\S+@\S+\.\S+$", email) is None:
        raise ValueError(f"'{email}' is not email address")
    return email
