from .devices import router as devices_router
from .main import router as main_router
from .products import router as products_router
from .stats import router as stats_router
from .task_lists import router as passages_router
from .tasks import router as tasks_router

routers = (
    main_router,
    products_router,
    devices_router,
    passages_router,
    tasks_router,
    stats_router
)

__all__ = ('routers',)
