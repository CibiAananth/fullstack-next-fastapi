import inspect
from typing import Callable

from core.cache.base import BaseKeyMaker


class CustomKeyMaker(BaseKeyMaker):
    async def make(self, function: Callable, prefix: str) -> str:
        module = inspect.getmodule(function)
        if module is None:
            raise ValueError("Function does not have a module.")

        path = f"{prefix}::{module.__name__}.{function.__name__}"
        args = ""

        for arg in inspect.signature(function).parameters.values():
            args += arg.name

        if args:
            return f"{path}.{args}"

        return path
