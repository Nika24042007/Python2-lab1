from typing import Protocol, runtime_checkable

@runtime_checkable
class Sources(Protocol):
    async def get_task(self) -> None: ...

    async def create_source(self, name:str) -> object: ...

    async def get_all_tasks(self) -> None: ...


