from enum import Enum
from functools import wraps

from sqlalchemy.ext.asyncio import AsyncSession

from core.db import session


class Propagation(Enum):
    REQUIRED = "required"
    REQUIRED_NEW = "required_new"


class Transactional:
    def __init__(self, propagation: Propagation = Propagation.REQUIRED):
        self.propagation = propagation

    def __call__(self, function):
        @wraps(function)
        async def decorator(*args, **kwargs):
            async with session() as s:  # s is an AsyncSession
                try:
                    if self.propagation == Propagation.REQUIRED:
                        result = await self._run_required(
                            s, function=function, args=args, kwargs=kwargs
                        )
                    elif self.propagation == Propagation.REQUIRED_NEW:
                        result = await self._run_required_new(
                            s, function=function, args=args, kwargs=kwargs
                        )
                    else:
                        result = await self._run_required(
                            s, function=function, args=args, kwargs=kwargs
                        )
                except Exception as exception:
                    await s.rollback()
                    raise exception
                else:
                    await s.commit()
                return result

        return decorator

    async def _run_required(
        self, session: AsyncSession, function, args, kwargs
    ) -> None:
        result = await function(*args, **kwargs)
        return result

    async def _run_required_new(
        self, session: AsyncSession, function, args, kwargs
    ) -> None:
        async with session.begin():
            result = await function(*args, **kwargs)
        return result
