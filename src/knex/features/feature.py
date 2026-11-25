from abc import ABC, abstractmethod
from typing import Any
from pydantic import BaseModel
from ..llm.llm import LLM
from ..llm.wrapper import Wrapper


class Feature(ABC, BaseModel):

    llm: Wrapper

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        pass
