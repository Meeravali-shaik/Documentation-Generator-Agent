import ast

def analyze_python(code):
    tree = ast.parse(code)
    functions = []
    calls = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)
        if isinstance(node, ast.Call) and hasattr(node.func, 'id'):
            calls.append(node.func.id)

    return functions, calls
