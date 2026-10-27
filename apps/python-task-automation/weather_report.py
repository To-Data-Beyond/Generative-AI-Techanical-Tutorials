import argparse
from urllib.parse import quote
import requests

def weather_report(location, session=None):
    location = location.strip()
    if not location or any(ord(c) < 32 for c in location):
        raise ValueError("Provide a nonempty location without control characters")
    http = session or requests
    response = http.get("https://wttr.in/" + quote(location, safe=""),
                        params={"T": ""}, timeout=(10, 30),
                        headers={"User-Agent": "curl/8.0"})
    response.raise_for_status()
    return response.text

def main():
    parser = argparse.ArgumentParser(description="Print a plain-text weather report from wttr.in.")
    parser.add_argument("location")
    args = parser.parse_args()
    try:
        print(weather_report(args.location))
    except (ValueError, requests.RequestException) as exc:
        parser.exit(1, f"Weather request failed: {exc}\n")

if __name__ == "__main__":
    main()
