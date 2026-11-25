# src/tests/test_llm_ollama.py
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from knex.llm import LLM, LLM_WRAPPERS

class TestLLMs(unittest.TestCase):

    def setUp(self):
        self.llms = [LLM(provider=p, model=p, api_key=p) for p in LLM_WRAPPERS.keys()]


    @patch("knex.llm.llm_ollama.chat")
    def test_message_text(self, chat):
        chat.return_value = SimpleNamespace(
            message=SimpleNamespace(
                content="Hello!"
            )
        )

        for llm in self.llms:
            answer = llm.message("Hello world")
            self.assertEqual(answer, "Hello!")


    @patch("knex.llm.llm_ollama.chat")
    def test_message_int(self, chat):
        chat.return_value = SimpleNamespace(
            message=SimpleNamespace(
                content="12"
            )
        )

        for llm in self.llms:
            answer = llm.message("Combien font 8 + 4", answer_type=int)

            self.assertEqual(answer, 12)
            self.assertIsInstance(answer, int)
            self.assertIsNotNone(chat.call_args.kwargs["format"])


if __name__ == "__main__":
    unittest.main()