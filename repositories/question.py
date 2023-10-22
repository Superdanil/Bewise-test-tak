from sqlalchemy import select, insert, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

import models


class QuestionRepository:
    """CRUD operations for table 'question'."""
    model = models.Question

    async def get_all_questions(self, session: AsyncSession) -> list[model]:
        stmt = select(self.model)
        result = await session.execute(stmt)
        questions = result.scalars().all()
        return list(questions)

    async def add_questions(self, new_questions: list[dict], session: AsyncSession) -> list[model] | None:
        stmt = insert(self.model).values(new_questions).returning(self.model)
        try:
            result = await session.execute(stmt)
            await session.commit()
            await session.close()
            return list(result.scalars().all())
        except IntegrityError:
            await session.close()

    async def delete_all_questions(self, session) -> None:
        stmt = delete(self.model)
        await session.execute(stmt)
        await session.commit()
