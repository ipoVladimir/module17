# В модуле db.py:
# Импортируйте все необходимые функции и классы , создайте движок указав пусть
# в БД - 'sqlite:///taskmanager.db' и локальную сессию (по аналогии с видео лекцией).
# Создайте базовый класс Base для других моделей, наследуясь от DeclarativeBase.

# Создаем начальную миграцию с alembic для существующей базы
# https://habr.com/ru/articles/585228/

# pip install alembic
# alembic init app/migrations
# Укажите адрес вашей базы данных 'sqlite:///taskmanager.db' в alembic.ini
# sqlalchemy.url = sqlite:///taskmanager.db
# В env.py импортируйте модели Base, User и Task. Целевой укажите Base.metadata
# from app.backend.db import Base
# from app.models import *
# target_metadata = Base.metadata
# alembic revision --autogenerate -m "Initial"
# alembic upgrade head

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine('sqlite:///taskmanager.db', echo=True)

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass


