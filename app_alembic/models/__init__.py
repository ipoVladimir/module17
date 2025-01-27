# Для более удобного импорта необходимо дополнить __init__.py в пакете models следующими строками:
# from .user import User from .task import Task
#
# Таким образом вы получите 2 модели связанные один(User) ко многим(Task).

from .user import User
from .task import Task