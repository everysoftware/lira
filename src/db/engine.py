from typing import Optional

from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine as create_async_engine_
from sqlalchemy.orm import sessionmaker

from src.config import cfg


def create_async_engine(url: URL | str) -> AsyncEngine:
    return create_async_engine_(url=url,
                                echo=cfg.debug,
                                pool_pre_ping=True)


def get_session_maker(engine: Optional[AsyncEngine] = None) -> sessionmaker:
    return sessionmaker(
        engine or create_async_engine(cfg.db.build_connection_str()),
        class_=AsyncSession,
        expire_on_commit=False
    )
