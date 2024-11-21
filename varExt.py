import os
import ast
import sys
from pathlib import Path
from flask import Flask, render_template, jsonify
from colorama import Fore, Style, init

# Initialize Colorama for cross-platform color support
init()

app = Flask(__name__)

def infer_type(node):
    """
    Infer the type of a variable based on its AST node.
    """
    if isinstance(node, ast.Constant):
        return type(node.value).__name__
    elif isinstance(node, ast.Str):
        return "str"
    elif isinstance(node, ast.Num):
        return "int" if isinstance(node.n, int) else "float"
    elif isinstance(node, ast.List):
        return "list"
    elif isinstance(node, ast.Dict):
        return "dict"
    elif isinstance(node, ast.Set):
        return "set"
    elif isinstance(node, ast.Tuple):
        return "tuple"
    elif isinstance(node, ast.Name):
        return "variable"
    elif isinstance(node, ast.Call):
        return "function_call"
    return "Unknown"

def extract_variables_with_context(file_path):
    """
    Parse a Python file and extract variables with function context or global status.
    """
    variables = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            file_content = file.read()
            tree = ast.parse(file_content, filename=file_path)

            current_function = None
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    current_function = node.name
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            var_name = target.id
                            var_type = infer_type(node.value) if hasattr(node, 'value') else "Unknown"
                            variables.append({
                                "Variable Name": var_name,
                                "Description": "",  # Placeholder
                                "Data Type": var_type,
                                "Default Value": getattr(node.value, "value", "(None)") if isinstance(node.value, ast.Constant) else "(None)",
                                "Example Usage": "",  # Placeholder
                                "Belongs To": f"Function: {current_function}" if current_function else "Global",
                                "File": str(file_path)
                            })
    except Exception as e:
        print(f"{Fore.RED}Error parsing {file_path}: {e}{Style.RESET_ALL}")
    return variables

def scan_codebase_for_variables_with_context(path):
    """
    Scan a file or directory for variables with context.
    """
    all_variables = []
    if os.path.isfile(path) and path.endswith(".py"):
        all_variables.extend(extract_variables_with_context(path))
    elif os.path.isdir(path):
        print(f"{Fore.CYAN}Scanning Python files in directory: {path}{Style.RESET_ALL}")
        for file_path in Path(path).rglob("*.py"):
            print(f"{Fore.GREEN}  Processing file: {file_path}{Style.RESET_ALL}")
            all_variables.extend(extract_variables_with_context(file_path))
    else:
        print(f"{Fore.RED}Invalid path. Provide a Python file or a folder containing Python files.{Style.RESET_ALL}")
        sys.exit(1)
    return all_variables

@app.route("/")
def home():
    """
    Serve the main webpage with the extracted variables.
    """
    global variables
    return render_template("variables.html", variables=variables)

@app.route("/api/variables")
def api_variables():
    """
    Provide an API endpoint to fetch variables as JSON.
    """
    global variables
    return jsonify(variables)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"{Fore.YELLOW}Usage: python3 varExt.py [folder or python file]{Style.RESET_ALL}")
        sys.exit(1)

    input_path = sys.argv[1]
    print(f"{Fore.MAGENTA}Scanning path: {input_path}{Style.RESET_ALL}")
    variables = scan_codebase_for_variables_with_context(input_path)

    print(f"{Fore.CYAN}Found {len(variables)} variables.{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Serving documentation on http://127.0.0.1:5000{Style.RESET_ALL}")
    app.run(debug=True)
