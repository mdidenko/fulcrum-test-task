import validators


def link_validator(link: str) -> bool:
    """Function to validate link."""
    return validators.url(link)
