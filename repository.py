from sqlalchemy import select

from database import new_session, TaskOrm
from schemas import STaskAdd, STask


class TaskRepository:
    @classmethod
    async def add_one(cls, data: STaskAdd) -> int:
        async with new_session() as session:
            task_dict = data.model_dump()

            task = TaskOrm(**task_dict)

            # добавляем объект в сессию (синхронная операция)
            session.add(task)

            # Отправляет изменения в базу, получит айдишник который новый первичный ключ (автоинкремент)
            await session.flush()

            # Сессия, все изменения этой сессии отправляются в бд
            await session.commit()
            return task.id

    # Получение всего списка задач
    @classmethod
    async def get_all(cls) -> list[STask]:
        # Объявили контекст менеджер сессии
        async with new_session() as session:
            # Обращаемся к таблице и делаем query запрос
            query = select(TaskOrm)

            # Обращаемся к БД через сессию и исполняем запрос query
            result = await session.execute(query)
            # Объект алхимии, который нам вернулся
            task_models = result.scalars().all()

            task_schemas  = [STask.model_validate(task_model) for task_model in task_models]


            return task_schemas 
