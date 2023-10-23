def is_strategy_key(key):
    excludes_key = [":remove", ":append", ":prepend", ":replace", ":rpm_macro_param"]
    if ":" not in key:
        return False
    if "when" in key:
        return False
    if "rpmWhen" in key:
        return False
    for exclude_item in excludes_key:
        if exclude_item in key:
            return False

    return True


def is_yaml_key(key):
    includes_key = [":rpm_macro_param", ":rpmWhen"]
    if ":" not in key:
        return True
    for include_item in includes_key:
        if include_item in key:
            return True

    return False
