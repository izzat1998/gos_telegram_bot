from aiogram.fsm.state import StatesGroup, State


class OrderStatistics(StatesGroup):
    list_by_status = State()
    detail = State()


class Workers(StatesGroup):
    type_of_worker = State()
    specialization = State()


