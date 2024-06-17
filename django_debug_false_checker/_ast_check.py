import ast
from typing import Any


class DebugTrueDetected(Exception): ...


class DebugTrueDetector(ast.NodeVisitor):
    def visit_Assign(self, node: ast.Assign) -> None:
        is_tuple = isinstance(node.value, ast.Tuple)
        for name_or_tuple in node.targets:
            if is_tuple:
                assert isinstance(name_or_tuple, ast.Tuple)
                assert isinstance(node.value, ast.Tuple)
                for name, value in zip(name_or_tuple.elts, node.value.elts):
                    if isinstance(name, ast.Expr):
                        continue
                    assert isinstance(name, ast.Name)
                    self._check_name_and_value(name, value)
            elif isinstance(name_or_tuple, ast.Name):
                self._check_name_and_value(name_or_tuple, node.value)
            else:
                # not handling ast.Expr
                continue

    def _check_name_and_value(self, name: ast.Name, value: Any):
        if name.id == "DEBUG" and isinstance(value, ast.Constant) and value.value:
            raise DebugTrueDetected()


def _ast_check(file_name: str, file_content: str) -> bool:
    content: ast.Module = ast.parse(file_content, filename=file_name)
    try:
        DebugTrueDetector().visit(content)
        return True
    except DebugTrueDetected:
        return False
