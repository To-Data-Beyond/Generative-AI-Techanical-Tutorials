import argparse
import re
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import requests

def convert_currency(amount, from_currency, to_currency, session=None):
    amount = Decimal(str(amount))
    if not amount.is_finite() or amount < 0:
        raise ValueError("Amount must be finite and nonnegative")
    base, quote = from_currency.upper(), to_currency.upper()
    if not all(re.fullmatch(r"[A-Z]{3}", c) for c in (base, quote)):
        raise ValueError("Use three-letter ISO currency codes")
    if base == quote:
        return amount, "same currency", Decimal("1")
    response = (session or requests).get(
        f"https://api.frankfurter.dev/v2/rate/{base}/{quote}", timeout=(10, 30))
    response.raise_for_status()
    data = response.json(parse_float=Decimal)
    if data["base"] != base or data["quote"] != quote:
        raise ValueError("Provider returned the wrong currency pair")
    rate = Decimal(str(data["rate"]))
    if not rate.is_finite() or rate <= 0:
        raise ValueError("Provider returned an invalid rate")
    return amount * rate, data["date"], rate

def main():
    parser = argparse.ArgumentParser(description="Convert using dated Frankfurter reference rates, not transaction quotes.")
    parser.add_argument("amount")
    parser.add_argument("from_currency")
    parser.add_argument("to_currency")
    args = parser.parse_args()
    try:
        result, date, rate = convert_currency(args.amount, args.from_currency, args.to_currency)
        rounded = result.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        print(f"{args.amount} {args.from_currency.upper()} = {rounded} {args.to_currency.upper()}")
        print(f"Rate date: {date}; rate: {rate}")
    except (ValueError, InvalidOperation, KeyError, requests.RequestException) as exc:
        parser.exit(1, f"Currency conversion failed: {exc}\n")

if __name__ == "__main__":
    main()
