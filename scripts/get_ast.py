# get_ast.py
import ast
import json
import sys

def code_to_ast_json(filepath):
    with open(filepath, "r") as f:
        source = f.read()
    
    # Parse into a native abstract syntax tree object
    tree = ast.parse(source)
    
    # Simple recursive walker to serialize the AST nodes into clean JSON
    def dump_node(node):
        fields = {}
        for k, v in ast.iter_fields(node):
            if isinstance(v, list):
                fields[k] = [dump_node(i) if isinstance(i, ast.AST) else str(i) for i in v]
            elif isinstance(v, ast.AST):
                fields[k] = dump_node(v)
            else:
                fields[k] = str(v)
        return {"type": node.__class__.__name__, **fields}

    return json.dumps(dump_node(tree), indent=2)

if __name__ == "__main__":
    # Dump the clean AST structural map directly to stdout
    print(code_to_ast_json(sys.argv[1]))
