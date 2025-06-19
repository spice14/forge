import ast
from pathlib import Path

def get_function_spans(file_path: Path):
    """
    Parse a .py file and return metadata about each top-level function or class method.
    """
    source = Path(file_path).read_text(encoding="utf-8")
    tree = ast.parse(source)

    results = []

    class FuncVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            start_line = node.lineno
            end_line = node.end_lineno if hasattr(node, 'end_lineno') else node.lineno
            name = node.name
            results.append({
                "filepath": file_path,
                "qualified_name": name,
                "start_line": start_line,
                "end_line": end_line,
            })

    FuncVisitor().visit(tree)
    return results
