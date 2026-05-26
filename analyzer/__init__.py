import ast

from .models import FunctionResult
from .parser import parse_source
from .patterns import SPACE_EXPLANATIONS, TIME_EXPLANATIONS
from .visitor import ComplexityVisitor


def analyze(source: str) -> list[FunctionResult]:
    tree = parse_source(source)
    results = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            visitor = ComplexityVisitor(node.name)
            visitor.visit(node)
            time_c = visitor.time_complexity()
            space_c = visitor.space_complexity()
            results.append(
                FunctionResult(
                    name=node.name,
                    time_complexity=time_c,
                    space_complexity=space_c,
                    explanation=f"{TIME_EXPLANATIONS[time_c]} {SPACE_EXPLANATIONS[space_c]}",
                )
            )
    return results
