from __future__ import annotations

import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from .common import init_db, insert_pulse, notify_admins_async


class PulseForm(StatesGroup):
    project = State()
    status = State()
    blocker = State()
    next_step = State()


bot = Bot(os.environ["PULSE_TOKEN"])
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Project Pulse is ready. Use /pulse to submit a GREEN, AMBER, or RED update.")


@dp.message(Command("pulse"))
async def pulse(message: Message, state: FSMContext) -> None:
    await state.set_state(PulseForm.project)
    await message.answer("Project ID or name?")


@dp.message(PulseForm.project)
async def project(message: Message, state: FSMContext) -> None:
    await state.update_data(project=message.text.strip())
    await state.set_state(PulseForm.status)
    await message.answer("Status? Reply GREEN, AMBER, or RED.")


@dp.message(PulseForm.status)
async def status(message: Message, state: FSMContext) -> None:
    value = message.text.strip().upper()
    if value not in {"GREEN", "AMBER", "RED"}:
        await message.answer("Use exactly GREEN, AMBER, or RED.")
        return
    await state.update_data(status=value)
    await state.set_state(PulseForm.blocker)
    await message.answer("Current blocker? Reply NONE if there is no blocker.")


@dp.message(PulseForm.blocker)
async def blocker(message: Message, state: FSMContext) -> None:
    await state.update_data(blocker=message.text.strip())
    await state.set_state(PulseForm.next_step)
    await message.answer("Next step and expected date?")


@dp.message(PulseForm.next_step)
async def finish(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    pulse_id = insert_pulse(message.from_user.id, data["project"], data["status"], data["blocker"], message.text.strip())
    text = (f"PROJECT PULSE #{pulse_id}\nProject: {data['project']}\nStatus: {data['status']}\n"
            f"Blocker: {data['blocker']}\nNext step: {message.text.strip()}\n"
            f"Reported by: @{message.from_user.username or message.from_user.id}")
    await notify_admins_async(bot, text)
    await message.answer(f"Pulse #{pulse_id} recorded and sent to the configured admins.")
    await state.clear()


@dp.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Pulse cancelled.")


async def main() -> None:
    init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
