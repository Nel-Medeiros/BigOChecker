import pytest
from analyzer import analyze
from analyzer.models import FunctionResult
from analyzer.parser import PythonSyntaxError


def test_analyze_single_function_returns_one_result():
    results = analyze("def foo(arr):\n for x in arr: pass")
    assert len(results) == 1


def test_analyze_single_function_name():
    results = analyze("def foo(arr):\n for x in arr: pass")
    assert results[0].name == "foo"


def test_analyze_single_function_time_complexity():
    results = analyze("def foo(arr):\n for x in arr: pass")
    assert results[0].time_complexity == "O(n)"


def test_analyze_multiple_functions():
    source = "def foo(): pass\ndef bar(arr):\n for x in arr: pass"
    results = analyze(source)
    assert len(results) == 2
    names = [r.name for r in results]
    assert "foo" in names
    assert "bar" in names


def test_analyze_no_functions_returns_empty_list():
    results = analyze("x = 1 + 1")
    assert results == []


def test_analyze_syntax_error_raises():
    with pytest.raises(PythonSyntaxError):
        analyze("def foo(: pass")


def test_analyze_result_is_function_result_instance():
    results = analyze("def foo(): pass")
    assert isinstance(results[0], FunctionResult)


def test_analyze_result_has_non_empty_explanation():
    results = analyze("def foo(): pass")
    assert results[0].explanation


def test_analyze_preserves_function_order():
    source = "def alpha(): pass\ndef beta(): pass\ndef gamma(): pass"
    results = analyze(source)
    assert [r.name for r in results] == ["alpha", "beta", "gamma"]


def test_analyze_only_top_level_functions():
    source = """
def outer(arr):
    def inner():
        pass
    for x in arr:
        pass
"""
    results = analyze(source)
    assert len(results) == 1
    assert results[0].name == "outer"
