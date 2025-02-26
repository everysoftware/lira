from aiogram import Router

from app.lists.router import router as checklists_router
from app.stats.router import router as stats_router
from app.tasks.router import router as tasks_router
from app.users.router import router as start_router
from app.voice.router import router as voice_router
from app.workspaces.router import router as devices_router

routers = [
    start_router,
    checklists_router,
    tasks_router,
    devices_router,
    stats_router,
    voice_router,
]

main_router = Router()
main_router.include_routers(*routers)
