import os
from .features import AssertionVerification, Assertification, NamedEntityRecognition
from .llm import LLM
from .preparation import prepare
from .pipeline import Pipeline

# Preparation

prepare()

llm = LLM(
    provider = os.getenv('LLM_PROVIDER', ''),
    model = os.getenv('LLM_MODEL', ''),
    api_key = os.getenv('LLM_API_KEY', '')
)


with open('src/temp/Suzanne Abbuehl.txt', 'r') as file:
    text = file.read()

with open('src/temp/Person - Birth and Death.ttl') as file:
    shacl = file.read()


Pipeline(llm, [
    Assertification, 
    # AssertionVerification,
    NamedEntityRecognition
]).run(text=text, shacl=shacl, save_path="src/temp")
