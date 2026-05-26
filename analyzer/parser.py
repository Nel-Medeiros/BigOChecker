import ast


class PythonSyntaxError(Exception):
    def __init__(self, message: str, line: int) -> None:
        self.message = message
        self.line = line
        super().__init__(message)


def parse_source(source: str) -> ast.Module:
    try:
        return ast.parse(source)
    except SyntaxError as e:
        raise PythonSyntaxError(message=e.msg, line=e.lineno or 0)
