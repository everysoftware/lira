import itertools
import logging
import os

from aiogram.fsm.context import FSMContext

from app.base.use_case import UseCase
from app.db.dependencies import UOWDep
from app.tasks.models import Task
from app.users.models import User
from app.voice.adapter import stt, ogg_to_wav
from app.voice.schemas import VoiceResponse, VoiceCommand

COMMAND_PATTERNS = {
    VoiceCommand.create_task: [
        ("создать", "создай", "создают", "добавить", "добавь", "добавляют"),
        ("задачи", "задачу", "задача", "задач"),
    ],
    VoiceCommand.show_tasks: [
        ("показать", "покажи"),
        ("задачи", "задачу", "задача", "задач"),
    ],
}


class VoiceUseCases(UseCase):
    def __init__(self, uow: UOWDep) -> None:
        self.uow = uow

    async def create_task(
        self, user: User, state: FSMContext, args: str
    ) -> None:
        user_data = await state.get_data()
        parts = args.split("добавь описание")
        name = parts[0].strip() if parts else ""
        desc = parts[1].strip() if len(parts) > 1 else None
        task = Task(
            name=name,
            description=desc,
            user_id=user.id,
            todo_list_id=user_data["todo_list_id"],
            workspace_id=user_data["workspace_id"],
        )
        await self.uow.tasks.add(task)
        await self.uow.commit()
        await state.update_data(task_id=str(task.id))

    async def help(
        self, user: User, state: FSMContext, ogg_path: str
    ) -> VoiceResponse:
        wav_path = ogg_path.replace(".ogg", ".wav")
        try:
            wav_path = ogg_to_wav(ogg_path, wav_path)
            text = stt(wav_path).lower()
            logging.info("Recognized text: %s", text)
            cmd = VoiceCommand.unknown
            pattern = ""

            for c, patterns in COMMAND_PATTERNS.items():
                for p_raw in itertools.product(*patterns):
                    p = " ".join(p_raw)
                    if p in text:
                        cmd = c
                        pattern = p
                        break

            args = text.replace(pattern, "").strip()
            match cmd:
                case VoiceCommand.create_task:
                    await self.create_task(user, state, args)
                case _:
                    pass

        except Exception as e:
            logging.info("Error: %s", e)
            raise
        finally:
            if os.path.exists(wav_path):
                os.remove(wav_path)

        return VoiceResponse(speech_text=text, cmd=cmd)
