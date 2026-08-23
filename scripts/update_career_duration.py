#!/usr/bin/env python3
import argparse
import datetime as dt
import re
from pathlib import Path


START_MARKER = "<!-- career-duration:start -->"
END_MARKER = "<!-- career-duration:end -->"
CAREER_START_YEAR = 2022
CAREER_START_MONTH = 7


def calculate_duration(start_year: int, start_month: int, today: dt.date) -> str:
    total_months = (today.year - start_year) * 12 + today.month - start_month
    if total_months < 0:
        raise ValueError("Current date cannot be earlier than the career start month.")

    years, months = divmod(total_months, 12)
    parts = [f"{years}년"] if years else []
    if months or not parts:
        parts.append(f"{months}개월")
    return " ".join(parts)


def update_readme(source: str, duration: str) -> str:
    pattern = re.compile(
        f"{re.escape(START_MARKER)}.*?{re.escape(END_MARKER)}",
        flags=re.DOTALL,
    )
    replacement = f"{START_MARKER}{duration}{END_MARKER}"
    updated, count = pattern.subn(replacement, source)
    if count != 1:
        raise ValueError("README must contain exactly one career duration marker pair.")
    return updated


def main() -> None:
    parser = argparse.ArgumentParser(description="Update career duration in README.md")
    parser.add_argument("readme", nargs="?", default="README.md", type=Path)
    args = parser.parse_args()

    source = args.readme.read_text(encoding="utf-8")
    duration = calculate_duration(CAREER_START_YEAR, CAREER_START_MONTH, dt.date.today())
    updated = update_readme(source, duration)
    if updated != source:
        args.readme.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    main()
