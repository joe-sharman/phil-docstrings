import attrs

from .types import ObjectType


@attrs.define
class PromptBuilder:
    include_description: bool
    include_args: bool
    include_return_types: bool
    include_exceptions: bool
    include_example_usage: bool

    def _get_prompt_intro(self, object_type: ObjectType) -> str:
        line_length = 75 if object_type == ObjectType.FUNCTION else 60
        return (
            f"Please write a detailed Python docstring for the following {object_type.value}."
            f" Limit line length to {line_length} characters. Keep the descriptions brief."
            " Only return docstring text (without quotation marks, backticks, or 'python') in your"
            f" response with no other parts of the {object_type.value}."
            " Include the following details:"
        )

    def _get_prompt_ending(self, code: str):
        return f"Here is the code:\n```python\n{code}"

    def _get_qualifiers(self, object_type: ObjectType) -> str:
        prompt = ""
        if self.include_description:
            prompt += f"\n - A brief overview of the purpose of the {object_type.value}."
        else:
            prompt += "\n - Do not include a description."
        if self.include_args:
            prompt += (
                "\n - Descriptions of input parameters, their types, and what they represent."
            )
        else:
            prompt += "\n - Do not include inputs args."
        if self.include_return_types:
            prompt += (
                "\n - The return type and what the returned value represents (if applicable)."
            )
        else:
            prompt += "\n - Do not include return types."
        if self.include_exceptions:
            prompt += "\n - Any exceptions raised (if applicable)."
        else:
            prompt += "\n - Do not include a exceptions."
        if self.include_example_usage:
            prompt += "\n - Example usage (if applicable)."
        else:
            prompt += "\n - Do not include an example usage."

        return prompt

    def build(self, code: str, object_type: ObjectType):
        prompt = self._get_prompt_intro(object_type)

        prompt += self._get_qualifiers(object_type)

        prompt += f"\n {self._get_prompt_ending(code)}"

        return prompt
