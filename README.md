Exercise in scraping of PyPI's simple API. 
Parse it using a Python script and extract some fun facts:
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
