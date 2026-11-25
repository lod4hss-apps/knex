
from logging import getLogger
from typing import Any
from .feature import Feature
from ..preparation import LogLevel

log = getLogger(__name__)


class Assertification(Feature):

    @staticmethod
    def get_params() -> list[str]:
        return ["text"]

    def execute(self, text: str):
        log.log(LogLevel.FEATURE, f"Text:\n{text}")

        prompt = "From the following text decompose it in small assertions of only subject, predicate, object (without complement).\n"
        prompt += "Make sure only one information is present in each assertions.\n"
        prompt += "Doing so, do not use pronons, all entities should be call by their names.\n"
        prompt += "Keep the original language.\n"
        prompt += f"Here is the text: {text}"

        answer = self.llm.message(prompt, answer_type=list[str])

        log.log(LogLevel.FEATURE, f"Answer:\n{'\n'.join(answer)}")
        return {"assertions": answer}


class AssertionVerification(Feature):

    @staticmethod
    def get_params() -> list[str]:
        return ["text", "assertions"]
    
    def execute(self, text: str, assertions: list[str]) :
        log.log(LogLevel.FEATURE, f"Text:\n{text}")

        prompt = 'From the following text, is the assertion: "{assertion}" correct?\n'
        prompt += f'Here is the text: "{text}"'

        correct_assertions = []
        wrong_assertions = []
        for assertion in assertions:
            log.log(LogLevel.FEATURE, f"Assertion: {assertion}")

            answer = self.llm.message(prompt.format(assertion=assertion), answer_type=bool)
            if answer: correct_assertions.append(assertion)
            else: wrong_assertions.append(assertion)

            log.log(LogLevel.FEATURE, f"==> {answer}")
        return {"assertions": correct_assertions, "wrong_assertions": wrong_assertions}