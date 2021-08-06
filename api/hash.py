import hashlib


def get_short_link_hash(link: str) -> str:
    """Function to get short hash from link."""
    md5_hash = hashlib.md5(link.encode()).hexdigest()
    return md5_hash[:6]
