from logging import getLogger
from typing import Any, TypeVar
from typing_extensions import TypeForm
from pydantic import PrivateAttr
from .wrapper import Wrapper
from .ollama_wrapper import OllamaWrapper
from ..preparation import LogLevel

T = TypeVar("T")
log = getLogger(__name__)

LLM_WRAPPERS = {
    "ollama": OllamaWrapper
}

class LLM(Wrapper):

    provider: str
    _llm: Wrapper = PrivateAttr()

    def model_post_init(self, context: Any) -> None:
        if self.provider not in LLM_WRAPPERS.keys():
            raise Exception(f'Unknown LLM provider <{self.provider}>; must be one of: {', '.join(LLM_WRAPPERS.keys())}')
        self._llm = LLM_WRAPPERS[self.provider](api_key=self.api_key, model=self.model)
        
    def message(self, prompt: str, system_prompt: str | None = None, answer_type: TypeForm[T] = str):
        log.log(LogLevel.LLM, f"{self.provider}/{self.model} message:\n==System==\n{system_prompt}\n==User==\n{prompt}")
        result = self._llm.message(prompt, system_prompt, answer_type)
        log.log(LogLevel.LLM, f"{self.provider}/{self.model} answer:\n{result}")
        return result