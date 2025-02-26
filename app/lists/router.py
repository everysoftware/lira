from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.base.pagination import LimitOffset
from app.base.types import UUID as ID, UUID
from app.lists.dependencies import TodoListServiceDep
from app.lists.keyboards import get_todo_list_kb, get_tasks_kb
from app.lists.states import TodoListGroup
from app.tasks.dependencies import TaskServiceDep
from app.tasks.states import TaskGroup
from app.users.dependencies import UserDep
from app.workspaces.dependencies import WorkspaceServiceDep
from app.workspaces.keyboards import get_workspace_kb

router = Router()


@router.message(F.text == "Списки 📝")
@router.message(Command("lists"))
@router.callback_query(F.data == "to_todo_lists")
async def get_many(
    event: types.Message | types.CallbackQuery,
    state: FSMContext,
    user: UserDep,
    todo_lists: TodoListServiceDep,
) -> None:
    message = (
        event.message if isinstance(event, types.CallbackQuery) else event
    )
    response = await todo_lists.get_many(user, LimitOffset(limit=100))
    kb = get_todo_list_kb(response)
    if response.total > 0:
        await message.answer(
            "Выберите список задач, чтобы переключиться", reply_markup=kb
        )
    else:
        await message.answer("Нет списков задач", reply_markup=kb)
    await state.set_state(TodoListGroup.get_many)
    if isinstance(event, types.CallbackQuery):
        await event.answer()


# GET
@router.message(F.text == "Задачи ✅")
@router.message(Command("tasks"))
@router.callback_query(F.data == "to_todo_list")
@router.callback_query(
    F.data.startswith("show_todo_list:"), TodoListGroup.get_many
)
async def get(
    event: types.CallbackQuery | types.Message,
    state: FSMContext,
    tasks: TaskServiceDep,
    todo_lists: TodoListServiceDep,
    *,
    todo_list_id: ID | None = None,
) -> None:
    if isinstance(event, types.CallbackQuery):
        message = event.message
        if event.data.startswith("show_"):
            todo_list_id = UUID(event.data.split(":")[1])
    else:
        message = event
    if todo_list_id is None:
        user_data = await state.get_data()
        todo_list_id = user_data["todo_list_id"]
    assert todo_list_id is not None

    response = await tasks.get_many(todo_list_id, LimitOffset(limit=100))
    kb = get_tasks_kb(response)
    todo_list = await todo_lists.get_one(todo_list_id)

    cap = (
        f"🗒 *{todo_list.name}*\n\n"
        f"Описание: {todo_list.description}\n"
        f"Теги: {todo_list.tags}\n"
        f"Создан: {todo_list.created_at}\n"
        f"Изменен: {todo_list.updated_at}\n\n"
    )
    if response.total > 0:
        await message.answer(cap + "Задачи", reply_markup=kb)
    else:
        await message.answer(cap + "Нет задач", reply_markup=kb)

    await state.update_data(
        workspace_id=str(todo_list.workspace_id),
        todo_list_id=str(todo_list.id),
    )
    await state.set_state(TaskGroup.get_many)
    if isinstance(event, types.CallbackQuery):
        await event.answer()


@router.callback_query(F.data == "add", TodoListGroup.get_many)
async def select_todo_list(
    call: types.CallbackQuery,
    state: FSMContext,
    user: UserDep,
    workspaces: WorkspaceServiceDep,
) -> None:
    page = await workspaces.get_many(user, LimitOffset(limit=100))
    kb = get_workspace_kb(page, action_btns=False)
    await call.message.answer(
        "Выберите пространство для списка задач", reply_markup=kb
    )
    await state.set_state(TodoListGroup.select_list)
    await call.answer()


@router.callback_query(F.data.startswith("select_"), TodoListGroup.select_list)
async def enter_name(call: types.CallbackQuery, state: FSMContext) -> None:
    workspace_id = call.data.split("_")[1]
    await state.update_data(workspace_id=workspace_id)
    await call.message.answer("Назовите список задач. Например, `фильмы`")
    await state.set_state(TodoListGroup.enter_name)
    await call.answer()


@router.message(TodoListGroup.enter_name)
async def enter_description(message: types.Message, state: FSMContext) -> None:
    await state.update_data(todo_list_name=message.text)
    await message.answer(
        "Введите описание. Например, `Фильмы, которые я хочу посмотреть`"
    )
    await state.set_state(TodoListGroup.enter_description)


@router.message(TodoListGroup.enter_description)
async def enter_stack(message: types.Message, state: FSMContext) -> None:
    await state.update_data(todo_list_description=message.text)
    await message.answer(
        "Введите теги. Они будут использованы для ИИ-анализа задач. "
    )
    await state.set_state(TodoListGroup.enter_stack)


@router.message(TodoListGroup.enter_stack)
async def add(
    message: types.Message,
    state: FSMContext,
    user: UserDep,
    todo_lists: TodoListServiceDep,
) -> None:
    tags = message.text
    user_data = await state.get_data()
    await todo_lists.create(
        user_id=user.id,
        workspace_id=user_data["workspace_id"],
        name=user_data["todo_list_name"],
        description=user_data["todo_list_description"],
        stack=tags,
    )
    await message.answer("Список успешно создан!")
    await get_many(message, state, user, todo_lists)
