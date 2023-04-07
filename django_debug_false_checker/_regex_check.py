import re

pattern = re.compile(r"DEBUG[\s]*=[\s]*True")


def _regex_check(_: str, file_content: str) -> bool:
    return not pattern.findall(file_content)
