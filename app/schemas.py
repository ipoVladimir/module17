# Создайте 4 схемы в модуле schemas.py, наследуемые от BaseModel,
# для удобной работы с будущими объектами БД:
# CreateUser с атрибутами: username(str), firstname(str), lastname(str) и age(int)
# UpdateUser с атрибутами: firstname(str), lastname(str) и age(int)
# CreateTask с атрибутами: title(str), content(str), priority(int)
# UpdateTask с теми же атрибутами, что и CreateTask.
# Обратите внимание, что 1/2 и 3/4 схемы обладают одинаковыми атрибутами.

from pydantic import BaseModel

class UpdateUser(BaseModel):
    firstname: str
    lastname: str
    age: int

class CreateUser(BaseModel, UpdateUser):
    username: str


class CreateTask(BaseModel):
    title: str
    content: str
    priority: int

class UpdateTask(BaseModel, CreateTask):
    pass

