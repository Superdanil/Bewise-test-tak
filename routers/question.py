from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas
from services import QuestionService

question_router = APIRouter(tags=["Questions"])


@question_router.get("/", response_model=list[schemas.Question])
async def get_all_questions(session: AsyncSession = Depends(models.session.scoped_session_dependency)):
    """Получить все записи таблицы 'question'."""
    question = QuestionService()
    return await question.get_all_questions(session=session)


@question_router.post("/", response_model=schemas.Question, status_code=status.HTTP_201_CREATED)
async def add_questions(
        questions_num: int,
        session: AsyncSession = Depends(models.session.scoped_session_dependency)
):
    """Добавляет сгенерированные вопросики из http://jservice.io/ в базу данных. Возвращает последний
    добавленный вопрос."""
    question = QuestionService()
    res = await question.add_questions(questions_num=questions_num, session=session)
    return res[-1]


@question_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_questions(session: AsyncSession = Depends(models.session.scoped_session_dependency)):
    """Очистить таблицу 'question'."""
    question = QuestionService()
    return await question.delete_all_questions(session=session)
