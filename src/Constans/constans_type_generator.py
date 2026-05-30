from typing import Any
from src.Task.task_api import TaskApi
from src.Task.task_file import TaskFile
from src.Task.task_generator import TaskGenerator

TYPE_GENERATOR: dict[str, Any] = {"file":TaskFile,
                                  "generator":TaskGenerator,
                                  "api":TaskApi}