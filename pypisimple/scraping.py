"""Simple index parsing"""

from functools import reduce
from html.parser import HTMLParser

import argparse
import json
import requests

# Issue with the cache for /simple/ not being purged often enough: https://github.com/pypa/warehouse/issues/7324
INDEX_URL = "https://pypi.org/simple/"
SAVE_FILE = "pypi.json"


class SimplePyPIHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.packages = []

    def handle_data(self, data):
        # Save data if it isn't a newline character.
        if len(data.strip()):
            self.packages.append(data)


def get_packages_array(offline):
    packages = []
    if offline:
        with open(SAVE_FILE, "r") as file:
            packages = json.load(file)
    else:
        r = requests.get(INDEX_URL)
        parser = SimplePyPIHTMLParser()
        parser.feed(r.text)
        parser.close()
        packages = parser.packages

        # Save into SAVE_FILE
        with open(SAVE_FILE, "w+") as file:
            json.dump(packages, file)

    return packages


def longest_name(packages_array):
    print("Get longest package name")
    lengths = [len(p) for p in packages_array]
    index = lengths.index(max(lengths))
    return packages_array[index]


def average_name_length(packages_array):
    print("Get average package name length")
    result = reduce(lambda acc, name: acc + len(name), packages_array, 0)
    return result / len(packages_array)


def package_name_contains(packages_array, substr):
    print(f"Check how many packages contain the string '{substr}'")
    result = 0
    for name in packages_array:
        if substr in name:
            result += 1
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compute some stats from scraping PyPI's simple API."
    )
    parser.add_argument(
        "-o",
        "--offline",
        action="store_true",
        help="Use saved data to compute the stats.",
    )
    args = parser.parse_args()
    offline = args.offline

    if offline:
        print("🔌 Offline parsing")

    packages = get_packages_array(offline)
    print(f"There are {len(packages)} packages listed on PyPI")

    longest_name = longest_name(packages)
    print(
        f"The longest package name is {longest_name} ({len(longest_name)} characters)."
    )

    avg_length = average_name_length(packages)
    print(f"The average package name length is {avg_length:.2f} characters.")

    strings = ["python", "py", "test"]
    for string in strings:
        contains_string = package_name_contains(packages, string)
        percentage = contains_string * 100 / len(packages)
        print(
            f"There are {contains_string} packages ({percentage:.2f}%) "
            f"that contain the string '{string}'."
        )
