"""Import all routers and add them to routers_list."""

from .admin import admin_router
from .echo import echo_router
from .orders import orders_router
from .user import user_router
from .workers import workers_router

routers_list = [
    admin_router,
    orders_router,
    workers_router,
    user_router,
    echo_router,  # echo_router must be last
]

__all__ = [
    "routers_list",
]
