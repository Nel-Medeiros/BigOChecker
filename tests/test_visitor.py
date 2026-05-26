import ast
from analyzer.visitor import ComplexityVisitor


def _analyze(source: str) -> ComplexityVisitor:
    """Parse source, find the first FunctionDef, run ComplexityVisitor on it."""
    tree = ast.parse(source)
    func = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef))
    visitor = ComplexityVisitor(func.name)
    visitor.visit(func)
    return visitor


def test_constant_function_time_is_o1():
    v = _analyze("def foo(x): return x + 1")
    assert v.time_complexity() == "O(1)"


def test_constant_function_space_is_o1():
    v = _analyze("def foo(x): return x + 1")
    assert v.space_complexity() == "O(1)"


def test_single_for_loop_is_on():
    v = _analyze("def foo(arr):\n for x in arr: pass")
    assert v.time_complexity() == "O(n)"


def test_single_while_loop_is_on():
    source = """
def foo(n):
    i = 0
    while i < n:
        i += 1
"""
    v = _analyze(source)
    assert v.time_complexity() == "O(n)"


def test_nested_for_loops_are_on2():
    source = """
def foo(arr):
    for i in arr:
        for j in arr:
            pass
"""
    v = _analyze(source)
    assert v.time_complexity() == "O(n²)"


def test_triple_nested_loops_are_on3():
    source = """
def foo(arr):
    for i in arr:
        for j in arr:
            for k in arr:
                pass
"""
    v = _analyze(source)
    assert v.time_complexity() == "O(n³)"


def test_binary_search_while_is_ologn():
    source = """
def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
"""
    v = _analyze(source)
    assert v.time_complexity() == "O(log n)"


def test_sorted_call_is_onlogn():
    v = _analyze("def foo(arr): return sorted(arr)")
    assert v.time_complexity() == "O(n log n)"


def test_sort_method_is_onlogn():
    source = """
def foo(arr):
    arr.sort()
    return arr
"""
    v = _analyze(source)
    assert v.time_complexity() == "O(n log n)"


def test_linear_recursion_is_on():
    source = """
def countdown(n):
    if n <= 0:
        return
    countdown(n - 1)
"""
    v = _analyze(source)
    assert v.time_complexity() == "O(n)"


def test_branching_recursion_is_o2n():
    source = """
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)
"""
    v = _analyze(source)
    assert v.time_complexity() == "O(2^n)"


def test_list_comprehension_space_is_on():
    v = _analyze("def foo(arr): return [x * 2 for x in arr]")
    assert v.space_complexity() == "O(n)"


def test_dict_comprehension_space_is_on():
    v = _analyze("def foo(arr): return {x: x*2 for x in arr}")
    assert v.space_complexity() == "O(n)"


def test_set_comprehension_space_is_on():
    v = _analyze("def foo(arr): return {x for x in arr}")
    assert v.space_complexity() == "O(n)"


def test_recursion_space_is_on():
    source = """
def fact(n):
    if n <= 1:
        return 1
    return n * fact(n - 1)
"""
    v = _analyze(source)
    assert v.space_complexity() == "O(n)"


def test_nested_list_comp_space_is_on2():
    source = """
def matrix(n):
    return [[0 for _ in range(n)] for _ in range(n)]
"""
    v = _analyze(source)
    assert v.space_complexity() == "O(n²)"


def test_no_collection_space_is_o1():
    v = _analyze("def foo(x): return x * 2")
    assert v.space_complexity() == "O(1)"


def test_floor_div_without_addition_is_not_ologn():
    source = """
def foo(n):
    i = 0
    while i < n:
        x = n // 2
        i += 1
"""
    v = _analyze(source)
    assert v.time_complexity() == "O(n)"
