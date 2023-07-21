from uuid import uuid4

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
)
from starlette.types import ASGIApp, Receive, Scope, Send

from core.db.session import reset_session_context, session, set_session_context


class SQLAlchemyMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        session_id = str(uuid4())
        context = set_session_context(session_id=session_id)

        try:
            await self.app(scope, receive, send)
        except Exception as exception:
            raise exception
        finally:
            if isinstance(session, async_scoped_session):
                await session.remove()
            elif isinstance(session, AsyncSession):
                await session.close()  # or some other method depending on what you want to do
            reset_session_context(context=context)
