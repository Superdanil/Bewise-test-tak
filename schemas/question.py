from datetime import datetime

from pydantic import BaseModel, ConfigDict


class QuestionGenerator(BaseModel):
    """Схема для генерации вопросов от стороннего API."""
    model_config = ConfigDict(from_attributes=True)  # свойства с атрибутов
    question: str
    answer: str


class Question(QuestionGenerator):
    """Схема для вопросов в БД."""
    id: int
    created_at: datetime
