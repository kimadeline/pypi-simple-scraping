# PyPI simple scraping 🥧🕵️‍♀️

Parse the content of the landing page of PyPI's simple API, and extract some ~~fun~~ facts:

- Longest package name
- Average package name length
- Number of packages with `py`, `python` and `test` in their name

# Setup

```bash
$ python -m venv .venv
$ source .venv/bin/activate
$ python -m pip install -r requirements.xt
$ python pypisimple/scraping.py
```

# Options

- `-o`, `--offline`: Computes stats from the cached data stored in `pypi.json` (gets updated every time the script isn't run in offline mode).
