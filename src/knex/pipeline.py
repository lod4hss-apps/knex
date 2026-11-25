import json, inspect
from logging import getLogger
from typing import Any
from .preparation import LogLevel
from .llm import LLM
from .features.feature import Feature

log = getLogger(__name__)


class Pipeline:

    def __init__(self, llm: LLM, tasks: list[type[Feature]]):
        self.llm = llm
        self.tasks = tasks
        log.log(LogLevel.PIPELINE, f"Pipeline initialized with {len(tasks)} features. Ready to run.")


    def run(self, save_path: str | None, **kwargs) -> dict[str, Any]:
        log.log(LogLevel.PIPELINE, '== PIPELINE STARTING == ')

        self.data = kwargs
        for i, Task in enumerate(self.tasks):
            log.log(LogLevel.PIPELINE, f"-- Running step {i+1}: {Task.__name__} -- ")
            task_instance = Task(llm=self.llm)
            task_param_names = list(inspect.signature(Task.execute).parameters)
            task_params = {key: value for key, value in self.data.items() if key in task_param_names}
            task_result = task_instance.execute(**task_params)
            self.data.update(task_result)

        if save_path: self.save(save_path)
        return self.data



    def save(self, path: str):
        with open(path + "/pipeline.json", "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)