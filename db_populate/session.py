from functools import wraps
from typing import TYPE_CHECKING

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings

if TYPE_CHECKING:
    from typing import Any
    from typing import Callable

async_engine = create_async_engine(settings.POSTGRES_CONNECTION_STRING, echo=settings.POSTGRES_ECHO)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)


def db_async_session_as_kwarg(func: 'Callable') -> 'Callable':
    @wraps(func)
    async def wrapper(*args: 'Any', **kwargs: 'Any') -> 'Any':
        async with async_session() as session:
            return await func(*args, **kwargs, session=session)

    return wrapper


engine = create_engine(settings.POSTGRES_CONNECTION_STRING, echo=settings.POSTGRES_ECHO)
session = sessionmaker(engine, expire_on_commit=False)


def db_session_as_kwarg(func: 'Callable') -> 'Callable':
    @wraps(func)
    def wrapper(*args: 'Any', **kwargs: 'Any') -> 'Any':
        with session() as _session:
            return func(*args, **kwargs, session=_session)

    return wrapper