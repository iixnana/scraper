def get_value(key, dictionary):
    return dictionary[key] if key in dictionary.keys() else None


def get_list(key, dictionary, split_str):
    return dictionary[key].split(split_str) if key in dictionary.keys() else [None, None]
