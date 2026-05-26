import ast


class ComplexityVisitor(ast.NodeVisitor):
    def __init__(self, func_name: str) -> None:
        self._func_name = func_name
        self._loop_depth = 0
        self._max_loop_depth = 0
        self._recursive_calls = 0
        self._has_halving = False
        self._has_sort = False
        self._creates_collection = False
        self._creates_2d = False

    def visit_For(self, node: ast.For) -> None:
        self._loop_depth += 1
        self._max_loop_depth = max(self._max_loop_depth, self._loop_depth)
        self.generic_visit(node)
        self._loop_depth -= 1

    def visit_While(self, node: ast.While) -> None:
        if self._has_floor_div(node):
            self._has_halving = True
        self._loop_depth += 1
        self._max_loop_depth = max(self._max_loop_depth, self._loop_depth)
        self.generic_visit(node)
        self._loop_depth -= 1

    def visit_Call(self, node: ast.Call) -> None:
        if isinstance(node.func, ast.Name) and node.func.id == self._func_name:
            self._recursive_calls += 1
        if isinstance(node.func, ast.Attribute) and node.func.attr == "sort":
            self._has_sort = True
        if isinstance(node.func, ast.Name) and node.func.id == "sorted":
            self._has_sort = True
        self.generic_visit(node)

    def visit_ListComp(self, node: ast.ListComp) -> None:
        if isinstance(node.elt, ast.ListComp):
            self._creates_2d = True
        self._creates_collection = True
        self.generic_visit(node)

    def visit_DictComp(self, node: ast.DictComp) -> None:
        self._creates_collection = True
        self.generic_visit(node)

    def visit_SetComp(self, node: ast.SetComp) -> None:
        self._creates_collection = True
        self.generic_visit(node)

    def time_complexity(self) -> str:
        if self._recursive_calls >= 2:
            return "O(2^n)"
        if self._max_loop_depth >= 3:
            return "O(n³)"
        if self._max_loop_depth == 2:
            return "O(n²)"
        if self._has_sort:
            return "O(n log n)"
        if self._has_halving and self._max_loop_depth <= 1:
            return "O(log n)"
        if self._max_loop_depth == 1 or self._recursive_calls == 1:
            return "O(n)"
        return "O(1)"

    def space_complexity(self) -> str:
        if self._creates_2d:
            return "O(n²)"
        if self._creates_collection or self._recursive_calls > 0:
            return "O(n)"
        return "O(1)"

    @staticmethod
    def _has_floor_div(node: ast.While) -> bool:
        return any(
            isinstance(child, ast.BinOp) and isinstance(child.op, ast.FloorDiv)
            for child in ast.walk(node)
        )
