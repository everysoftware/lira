from typing import Annotated

from fast_depends import Depends

from app.lists.service import TodoListUseCases

TodoListServiceDep = Annotated[TodoListUseCases, Depends(TodoListUseCases)]
