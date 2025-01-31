# В модуле user.py напишите APIRouter с префиксом '/user' и тегом 'user', а также следующие маршруты, с пустыми функциями:
# get '/' с функцией all_users.
# get '/user_id' с функцией user_by_id.
# post '/create' с функцией create_user.
# put '/update' с функцией update_user.
# delete '/delete' с функцией delete_user.

# Задача "Маршрутизация пользователя":
# Необходимо описать логику функций в user.py используя ранее написанные маршруты FastAPI.
# Подготовка:
#
#     Для этого задания установите в виртуальное окружение пакет python-slugify.
#     Скачайте этот файл, в нём описана функция-генератор для подключения к БД. Добавьте его в директорию backend.
#
# Подготовьтесь и импортируйте все необходимые классы и функции (ваши пути могут отличаться):
# from fastapi import APIRouter, Depends, status, HTTPException
# # Сессия БД
# from sqlalchemy.orm import Session
# # Функция подключения к БД
# from backend.db_depends import get_db
# # Аннотации, Модели БД и Pydantic.
# from typing import Annotated
# from models import User
# from schemas import CreateUser, UpdateUser
# # Функции работы с записями.
# from sqlalchemy import insert, select, update, delete
# # Функция создания slug-строки
# from slugify import slugify
#
# Напишите логику работы функций маршрутов:
# Каждая из нижеперечисленных функций подключается к базе данных в момент обращения при помощи функции get_db - Annotated[Session, Depends(get_db)]
# Функция all_users ('/'):
#
#     Должна возвращать список всех пользователей из БД. Используйте scalars, select и all
#
# Функция user_by_id ('/user_id'):
# Для извлечения записи используйте ранее импортированную функцию select.
#
#     Дополнительно принимает user_id.
#     Выбирает одного пользователя из БД.
#     Если пользователь не None, то возвращает его.
#     В противном случае выбрасывает исключение с кодом 404 и описанием "User was not found"
#
# Функция craete_user ('/create'):
# Для добавления используйте ранее импортированную функцию insert.
#
#     Дополнительно принимает модель CreateUser.
#     Подставляет в таблицу User запись значениями указанными в CreateUser.
#     В конце возвращает словарь {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}
#     Обработку исключения существующего пользователя по user_id или username можете сделать по желанию.
#
# Функция update_user ('/update'):
# Для обновления используйте ранее импортированную функцию update.
#
#     Дополнительно принимает модель UpdateUser и user_id.
#     Если находит пользователя с user_id, то заменяет эту запись значениям из модели UpdateUser. Далее возвращает словарь {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}
#     В противном случае выбрасывает исключение с кодом 404 и описанием "User was not found"
#
# Функция delete_user ('/delete'):
# Для удаления используйте ранее импортированную функцию delete.
#
#     Всё должно работать аналогично функции update_user, только объект удаляется.
#     Исключение выбрасывать то же.

# pip install python-slugify

from fastapi import APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.models import *
from app.schemas import CreateUser, UpdateUser
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify

router = APIRouter(prefix="/user", tags=["user"])

# Каждая из нижеперечисленных функций подключается к базе данных в момент обращения
# при помощи функции get_db - Annotated[Session, Depends(get_db)]
# Функция all_users ('/'):
# Должна возвращать список всех пользователей из БД. Используйте scalars, select и all
@router.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    if users is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no users'
        )
    return users

# Функция user_by_id ('/user_id'):
# Для извлечения записи используйте ранее импортированную функцию select.
#     Дополнительно принимает user_id.
#     Выбирает одного пользователя из БД.
#     Если пользователь не None, то возвращает его.
#     В противном случае выбрасывает исключение с кодом 404 и описанием "User was not found"
@router.get("/user_id")
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    usr = db.scalar(select(User).where(User.id==user_id))
    if usr is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
    return usr

@router.post("/create")
async def create_user(db: Annotated[Session, Depends(get_db)], create_user: CreateUser):
    usr = db.scalar(select(User).where(User.username == create_user.username))
    if usr is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with username '{create_user.username}' already exists"
        )

    db.execute(insert(User).values(username=create_user.username,
                                      firstname=create_user.firstname,
                                      lastname=create_user.lastname,
                                      age=create_user.age,
                                      slug=slugify(create_user.username)))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }

# Функция update_user ('/update'):
# Для обновления используйте ранее импортированную функцию update.
#     Дополнительно принимает модель UpdateUser и user_id.
#     Если находит пользователя с user_id, то заменяет эту запись значениям из модели UpdateUser.
#     Далее возвращает словарь {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}
#     В противном случае выбрасывает исключение с кодом 404 и описанием "User was not found"
@router.put("/update")
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int, update_user: UpdateUser):
    usr = db.scalar(select(User).where(User.id == user_id))
    if usr is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found"
        )

    db.execute(update(User).where(User.id == user_id).values(
        firstname = update_user.firstname,
        lastname = update_user.lastname,
        age = update_user.age))

    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User update is successful!'
    }

# Функция delete_user ('/delete'):
# Для удаления используйте ранее импортированную функцию delete.
#     Всё должно работать аналогично функции update_user, только объект удаляется.
#     Исключение выбрасывать то же.
@router.delete("/delete")
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    usr = db.scalar(select(User).where(User.id == user_id))
    if usr is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found"
        )

    db.execute(delete(User).where(User.id == user_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User delete is successful!'
    }