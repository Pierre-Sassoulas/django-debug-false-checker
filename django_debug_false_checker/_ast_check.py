import ast


def _ast_check(file_name: str, file_content: str) -> bool:
    content: ast.Module = ast.parse(file_content, filename=file_name)
    for node in content.body:
        if not isinstance(node, ast.Assign):
            continue
        for name in node.targets:
            if name.id != "DEBUG" or not node.value.value:  # type: ignore[attr-defined]
                continue
            return False
    return True
