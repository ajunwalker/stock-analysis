THOUSAND = 1_000
MILLION = 1_000 * THOUSAND
BILLION = 1_000 * MILLION
TRILLION = 1_000 * BILLION


def format_number(number: int | float) -> str:
    if abs(number) > TRILLION:
        return str(round(number / TRILLION, 2)) + "T"
    elif abs(number) > BILLION:
        return str(round(number / BILLION, 2)) + "B"
    elif abs(number) > MILLION:
        return str(round(number / MILLION, 2)) + "M"
    elif abs(number) > THOUSAND:
        return str(round(number / THOUSAND, 2)) + "K"

    return str(round(number, 2))
