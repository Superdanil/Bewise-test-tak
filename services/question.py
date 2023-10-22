import httpx
from pydantic import ValidationError

import schemas
from repositories.question import QuestionRepository


class QuestionService:
    def __init__(self):
        self.repository = QuestionRepository()

    async def add_questions(self, questions_num: int, session) -> list:
        result = await self.generate_unique_questions(questions_num=questions_num, session=session)
        while not result:
            result = await self.generate_unique_questions(questions_num=questions_num, session=session)
        return result

    async def generate_unique_questions(self, questions_num: int, session):
        new_questions = await self.generate_questions(questions_num=questions_num)
        new_questions = self.remove_keys(new_questions, keys_to_keep=['question', 'answer'])
        result = await self.repository.add_questions(new_questions=new_questions, session=session)
        return result

    async def delete_all_questions(self, session):
        try:
            await self.repository.delete_all_questions(session=session)
        except Exception as e:
            print(e)

    async def get_all_questions(self, session):
        try:
            res = await self.repository.get_all_questions(session=session)
            return res
        except Exception as e:
            print(e)

    @staticmethod
    async def generate_questions(questions_num: int) -> list[schemas.QuestionGenerator]:
        async with httpx.AsyncClient() as client:
            url = "http://jservice.io/"
            response = await client.get(f"{url}api/random?count={questions_num}")
            response = response.json()
            for i in response:
                try:
                    schemas.QuestionGenerator(question=i['question'], answer=i['answer'])
                except ValidationError as e:
                    print(e)
                    print(f"Ошибка валидации от {url}")
            return response

    @staticmethod
    def remove_keys(questions_list: list[dict], keys_to_keep: list[str]) -> list[dict]:
        for dictionary in questions_list:
            keys_to_remove = [key for key in dictionary.keys() if key not in keys_to_keep]
            for key in keys_to_remove:
                dictionary.pop(key)
        return questions_list
