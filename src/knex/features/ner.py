from logging import getLogger
from rdflib import Graph
from rdflib.graph import _SubjectType
from rdflib.term import Identifier
from .feature import Feature
from ..preparation import LogLevel

log = getLogger(__name__)


class NamedEntityRecognition(Feature):

    @staticmethod
    def get_params() -> list[str]:
        return ["assertion"]

    
    def execute(self, assertions: list[str], shacl: str):

        classes_names = self.__get_class_name_list(shacl)

        prompt = f"List all instances of {', '.join(classes_names)} from the following assertion. Note that date have\n"
        prompt += "Format is: [{{'text': <original_text>, 'class': <class_name>}}, ...]\n"
        prompt += 'Assertion: "{assertion}"'
        
        entities = []
        for assertion in assertions:
            log.log(LogLevel.FEATURE, f"Assertion: {assertion}")
            answer = self.llm.message(prompt.format(assertion=assertion), answer_type=list[dict[str, str]])

            log.log(LogLevel.FEATURE, f"Entities: {'; '.join([f"{e['text']} ({e['class']})" for e in answer])}")
            entities += answer
        
        return {"entities": entities}


    def __get_class_name_list(self, shacl: str) -> list[str]:
        graph = Graph()
        graph.parse(data=shacl, format='turtle')


        rows = graph.query("select ?class_name where {?shape a sh:NodeShape; sh:name ?class_name}")

        result = []
        for row in rows:
            if not isinstance(row, bool) and isinstance(row[0], str):
                result.append(row[0])

        return result