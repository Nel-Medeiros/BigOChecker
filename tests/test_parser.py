import ast
import pytest
from analyzer.parser import parse_source, PythonSyntaxError


def test_valid_source_returns_ast_module():
    tree = parse_source("def foo(): pass")
    assert isinstance(tree, ast.Module)


def test_valid_source_with_multiple_functions():
    tree = parse_source("def foo(): pass\ndef bar(): pass")
    func_names = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    assert "foo" in func_names
    assert "bar" in func_names


def test_syntax_error_raises_python_syntax_error():
    with pytest.raises(PythonSyntaxError):
        parse_source("def foo(: pass")


def test_syntax_error_carries_line_number():
    with pytest.raises(PythonSyntaxError) as exc_info:
        parse_source("def foo(: pass")
    assert exc_info.value.line > 0


def test_syntax_error_carries_message():
    with pytest.raises(PythonSyntaxError) as exc_info:
        parse_source("def foo(: pass")
    assert exc_info.value.message
