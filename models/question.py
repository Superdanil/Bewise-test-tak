from asyncio import current_task
from datetime import datetime

from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session
)
from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy.orm import Mapped, mapped_column

from schemas import question


class Base(DeclarativeBase):
    """Базовый класс для моделей базы данных"""
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class Question(Base):
    """Таблица question в базе данных"""
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question: Mapped[str] = mapped_column(String, unique=True)
    answer: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True
    )


class AsyncDatabaseSession:
    def __init__(self, url: str):
        self.engine = create_async_engine(
            url=url,
            echo=True
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False
        )

    def get_scoped_session(self):
        sess = async_scoped_session(session_factory=self.session_factory, scopefunc=current_task)
        return sess

    async def session_dependency(self) -> AsyncSession:
        async with self.session_factory() as sess:
            yield sess
            await sess.close()

    async def scoped_session_dependency(self) -> AsyncSession:
        sess = self.get_scoped_session()
        yield sess
        await sess.close()


session = AsyncDatabaseSession("postgresql+asyncpg://postgres:postgres@localhost/bewise_db")
