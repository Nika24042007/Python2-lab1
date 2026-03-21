from typing import Protocol, runtime_checkable

@runtime_checkable
class Sources(Protocol):
    def get_task(self) -> str: ...

    def create_source(self, name:str) -> object: ...

    def get_all_tasks(self) -> str: ...


