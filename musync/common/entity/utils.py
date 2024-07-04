import re


def normalize_str(string: str) -> str:
    """
    Normalize a string by lowercasing it, removing special characters,
    and removing extra whitespace.

    Parameters
    ----------
    string : str
        The string to normalize.

    Returns
    -------
    str
        The normalized string.
    """
    string = string.lower()
    string = re.sub(r"[-()]", "", string)
    string = re.sub(r"\s+", " ", string)
    string = string.strip()
    return string
