import ast
import os

import attrs

from .model import Model
from .prompt import PromptBuilder
from .types import ObjectType


@attrs.define
class DocstringInserter:
    module_path: str
    output_path: str
    model: Model
    prompt_builder: PromptBuilder

    def generate_docstring(self, code: str, object_type: ObjectType):
        prompt = self.prompt_builder.build(code, object_type)
        response = self.model.generate(prompt)
        return response

    def _can_generate(self, node) -> bool:
        if not node.body:
            return False
        if not isinstance(node.body[0], ast.Expr):
            return False
        if not isinstance(node.body[0].value, ast.Constant):
            return False
        if not isinstance(node.body[0].value.value, str):
            return False
        return True

    def visit_and_add_docstrings(self, node):
        """Walks the AST, adds docstrings to functions and classes."""
        for child in ast.iter_child_nodes(node):


            if isinstance(child, ast.FunctionDef):
                docstring = self.generate_docstring(child, ObjectType.FUNCTION)
            elif isinstance(child, ast.ClassDef):
                docstring = self.generate_docstring(child, ObjectType.CLASS)
            else:
                continue

            docstring_node = ast.Expr(value=ast.Constant(value=docstring))
            child.body.insert(0, docstring_node)

            self.visit_and_add_docstrings(child)

    def run(self):
        """Main function to process a module and write output."""
        with open(self.module_path, "r") as f:
            code = f.read()

        tree = ast.parse(code)
        self.visit_and_add_docstrings(tree)

        new_code = ast.unparse(tree)

        directory = os.path.dirname(self.output_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        with open(self.output_path, "w") as f:
            f.write(new_code)
