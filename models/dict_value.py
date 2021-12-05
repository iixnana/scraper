import re


def get_value(key, dictionary):
    return dictionary[key] if key in dictionary.keys() else None


def get_list(key, dictionary, split_str):
    return dictionary[key].split(split_str) if key in dictionary.keys() else [None, None]


def clean_html(raw_html):
    return _RE_COMBINE_WHITESPACE.sub(" ", raw_html.text).strip() if raw_html is not None else None


def clean_str(raw_str):
    return _RE_COMBINE_WHITESPACE.sub(" ", raw_str).strip() if raw_str is not None else None


_RE_COMBINE_WHITESPACE = re.compile(r"\s+")
