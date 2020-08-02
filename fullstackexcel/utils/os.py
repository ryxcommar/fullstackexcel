import re
import os


def parse_config_val(s: str) -> str:
    """Returns a value that may or may not be an environment variable. A value
    is an environment variable if it is wrapped in percent signs, e.g. %USER%.
    Obviously, we use the percent notation instead of dollar signs because this
    is a Windows product, and we want Powershell users to feel at home. (Sorry,
    bash users!) If the value is not wrapped in percent signs, simply return
    the value that was input.
    """
    try:
        regex = re.match('^%(.*?)%$', s)
    except TypeError:
        pass
    else:
        if regex:
            return os.getenv(regex[1])
    return s


def parse_config(d: dict) -> dict:
    return {k: parse_config_val(v) for k, v in d.items()}
