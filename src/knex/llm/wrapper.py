from typing import TypeVar
from typing_extensions import TypeForm
from abc import ABC, abstractmethod
from pydantic import BaseModel

T = TypeVar("T")

class Wrapper(ABC, BaseModel):

    model: str
    api_key: str | None

    @abstractmethod
    def message(self, prompt: str, system_prompt: str | None = None, answer_type: TypeForm[T] = str) -> T:
        pass

