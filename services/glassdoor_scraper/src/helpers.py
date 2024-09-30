from utils.logging import logger

def format_reviews_string(reviews_string: str) -> int:
    """
    Format the reviews string to a numeric value.
    Does not handle the case where the reviews are in the millions.
    Params:
    - reviews_string: str - the string to format.

    Returns:
    - int: The numeric value of the reviews.
    """
    try:
        numeric_value = float(reviews_string.split()[0].replace(",", "."))
        if "mil" in reviews_string:
            numeric_value *= 1000
    except Exception as e:
        logger.error(f"Error formatting reviews string: {e}")
        numeric_value = 0
    return int(numeric_value)
