from typing import TypeVar

from ollama import chat
from pydantic import TypeAdapter
from typing_extensions import TypeForm

from .wrapper import Wrapper

T = TypeVar("T")


class OllamaWrapper(Wrapper):

    def message(self, prompt: str, system_prompt: str | None = None, answer_type: TypeForm[T] = str) -> T:
        messages = []
        if system_prompt: messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        adapter = TypeAdapter(answer_type)
        format = adapter.json_schema() if answer_type != str else None

        response = chat(model=self.model, messages=messages, format=format)
        answer = response.message.content or ''

        if answer_type is str: return adapter.validate_python(answer)
        else: return adapter.validate_json(answer)