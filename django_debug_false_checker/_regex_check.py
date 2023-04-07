import re

pattern = re.compile(r"DEBUG = True")


def _regex_check(_: str, file_content: str) -> bool:
    return not pattern.findall(file_content)
