from types import SimpleNamespace
from .assertification import Assertification, AssertionVerification
from .ner import NamedEntityRecognition

FEATURES = SimpleNamespace(
    Assertification=Assertification,
    AssertVerification=AssertionVerification,
    NamedEntityRecognition=NamedEntityRecognition
)