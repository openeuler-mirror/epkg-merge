def is_strategy_key(key):
    excludes_key = [":remove", ":append", ":prepend", ":replace", ":rpm_macro_param"]
    if ":" not in key:
        return False
    if "@" in key:
        return False
    for exclude_item in excludes_key:
        if exclude_item in key:
            return False

    return True


def is_yaml_key(key):
    excludes_key = [":remove", ":append", ":prepend", ":replace"]
    if ":" not in key:
        return True
    for exclude_item in excludes_key:
        if exclude_item in key:
            return False
    if ":rpm_macro_param" in key:
        return True
    else:
        return False
