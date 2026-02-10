from __future__ import annotations

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


# --- Core dictionaries for word conversion ---
ONES_AND_TEENS = {
    0: "zero", 1: "one", 2: "two", 3: "three", 4: "four",
    5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
    10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen",
    15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen",
}

TENS = {
    20: "twenty", 30: "thirty", 40: "forty", 50: "fifty",
    60: "sixty", 70: "seventy", 80: "eighty", 90: "ninety",
}

SCALES = ["", "thousand", "million", "billion"]  # supports up to 999,999,999,999


def parse_money(amount_str: str) -> tuple[int, int]:
    """
    Convert a user-supplied money string into integer dollars and cents.
    Uses Decimal to avoid float rounding issues.

    Examples:
      "123.45" -> (123, 45)
      "10"     -> (10, 0)
      "0.9"    -> (0, 90)
    """
    cleaned = amount_str.strip().replace(",", "")
    if not cleaned:
        raise ValueError("Empty amount.")

    try:
        amt = Decimal(cleaned)
    except InvalidOperation as exc:
        raise ValueError("Invalid numeric amount.") from exc

    if amt < 0:
        raise ValueError("Amount must be non-negative.")

    # Round to exactly two decimals (typical money rounding)
    amt = amt.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    dollars = int(amt)  # Decimal to int truncates toward 0 (safe here, amt >= 0)
    cents = int((amt - Decimal(dollars)) * 100)

    # Guard against any weird edge cases
    if cents < 0 or cents > 99:
        raise ValueError("Cents out of range after rounding.")

    if dollars > 999_999_999_999:
        raise ValueError("Amount too large (max is 999,999,999,999.99).")

    return dollars, cents


def two_digit_to_words(n: int) -> str:
    """Convert an integer 0..99 into words."""
    if not (0 <= n <= 99):
        raise ValueError("two_digit_to_words expects 0..99")

    if n < 20:
        return ONES_AND_TEENS[n]

    tens_part = (n // 10) * 10
    ones_part = n % 10

    if ones_part == 0:
        return TENS[tens_part]
    return f"{TENS[tens_part]}-{ONES_AND_TEENS[ones_part]}"


def three_digit_to_words(n: int) -> str:
    """Convert an integer 0..999 into words."""
    if not (0 <= n <= 999):
        raise ValueError("three_digit_to_words expects 0..999")

    if n == 0:
        return ""

    hundreds = n // 100
    remainder = n % 100

    parts: list[str] = []
    if hundreds:
        parts.append(f"{ONES_AND_TEENS[hundreds]} hundred")
    if remainder:
        parts.append(two_digit_to_words(remainder))

    return " ".join(parts)


def int_to_words(n: int) -> str:
    """Convert an integer 0..999,999,999,999 into words."""
    if n == 0:
        return "zero"
    if not (0 <= n <= 999_999_999_999):
        raise ValueError("int_to_words expects 0..999,999,999,999")

    parts: list[str] = []
    scale_index = 0
    remaining = n

    while remaining > 0:
        group = remaining % 1000  # take last 3 digits
        remaining //= 1000

        if group:
            group_words = three_digit_to_words(group)
            scale_word = SCALES[scale_index]
            if scale_word:
                parts.append(f"{group_words} {scale_word}".strip())
            else:
                parts.append(group_words)

        scale_index += 1

    # groups were built from lowest scale to highest, so reverse
    return " ".join(reversed(parts)).strip()


def format_check_words(dollars: int, cents: int) -> str:
    """Assemble the final check-writing string."""
    dollar_words = int_to_words(dollars)
    cent_words = two_digit_to_words(cents)

    dollar_unit = "dollar" if dollars == 1 else "dollars"
    cent_unit = "cent" if cents == 1 else "cents"

    sentence = f"{dollar_words} {dollar_unit} and {cent_words} {cent_unit}"

    # Checks usually start with a capital letter
    return sentence[0].upper() + sentence[1:]


def main() -> None:
    print("Check Writer (number -> words)")
    user_input = input("Enter amount (e.g., 123.45): ").strip()

    try:
        dollars, cents = parse_money(user_input)
        result = format_check_words(dollars, cents)
        print(result)
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
