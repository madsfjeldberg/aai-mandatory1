from __future__ import annotations

import argparse
import csv
from pathlib import Path


BRAND_ALIASES = {
    "chevy": "chevrolet",
    "chevroelt": "chevrolet",
    "maxda": "mazda",
    "mercedes benz": "mercedes-benz",
    "toyouta": "toyota",
    "vokswagen": "volkswagen",
    "vw": "volkswagen",
}

MULTI_WORD_BRANDS = {"mercedes benz"}


def split_car_name(car_name: str) -> tuple[str, str]:
    tokens = car_name.strip().split()
    if not tokens:
        return "", ""

    if len(tokens) >= 2:
        first_two = f"{tokens[0].lower()} {tokens[1].lower()}"
        if first_two in MULTI_WORD_BRANDS:
            brand = BRAND_ALIASES.get(first_two, " ".join(tokens[:2]))
            model = " ".join(tokens[2:])
            return brand, model

    first = tokens[0].lower()
    brand = BRAND_ALIASES.get(first, tokens[0])
    model = " ".join(tokens[1:])
    return brand, model


def transform_csv(input_path: Path, output_path: Path) -> None:
    with input_path.open(newline="", encoding="utf-8") as input_file:
        reader = csv.DictReader(input_file)
        fieldnames = [name for name in reader.fieldnames or [] if name != "car name"]
        fieldnames.extend(["car brand", "car model"])

        with output_path.open("w", newline="", encoding="utf-8") as output_file:
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                brand, model = split_car_name(row.get("car name", ""))
                row.pop("car name", None)
                row["car brand"] = brand
                row["car model"] = model
                writer.writerow(row)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Split the 'car name' CSV column into brand and model columns.",
    )
    parser.add_argument(
        "input_csv",
        nargs="?",
        default="cars_split.csv",
        help="Path to the input CSV file.",
    )
    parser.add_argument(
        "output_csv",
        nargs="?",
        default="cars_split_out.csv",
        help="Path to the output CSV file.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    transform_csv(Path(args.input_csv), Path(args.output_csv))


if __name__ == "__main__":
    main()