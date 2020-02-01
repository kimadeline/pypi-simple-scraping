"""Simple index parsing"""

from functools import reduce
from html.parser import HTMLParser
import requests

INDEX_URL = "https://pypi.org/simple/"


class SimplePyPIHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.packages = []

    def handle_data(self, data):
        # if it isn't a newline character
        if len(data.strip()):
            self.packages.append(data)


def get_packages_array(url):
    r = requests.get(url)
    parser = SimplePyPIHTMLParser()
    parser.feed(r.text)
    parser.close()

    return parser.packages


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


packages = get_packages_array(INDEX_URL)

print(f"There are {len(packages)} packages listed on PyPI")

avg_length = average_name_length(packages)

print(f"The average package name length is {avg_length:.2f} characters")

strings = ["python", "py", "test"]
for string in strings:
    contains_string = package_name_contains(packages, string)
    percentage = contains_string * 100 / len(packages)
    print(
        f"There are {contains_string} packages ({percentage:.2f}%) "
        f"that contain the string '{string}'"
    )
