from __future__ import annotations

import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from .common import init_db, insert_access, notify_admins_async


class AccessForm(StatesGroup):
    tier = State()
    scope = State()
    role = State()


bot = Bot(os.environ["CONCIERGE_TOKEN"])
dp = Dispatcher()


def tier_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Tier 2 — Community", callback_data="tier:Tier 2")],
        [InlineKeyboardButton(text="Tier 3 — Contributor", callback_data="tier:Tier 3")],
        [InlineKeyboardButton(text="Tier 4 — Leadership", callback_data="tier:Tier 4")],
    ])


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Welcome to TECHIES COMMUNITY. I can collect a room access request. Use /request_access to begin.")


@dp.message(Command("request_access"))
async def request_access(message: Message, state: FSMContext) -> None:
    await state.set_state(AccessForm.tier)
    await message.answer("Which access tier are you requesting? Tier 4 requests are always manually approved.", reply_markup=tier_keyboard())


@dp.callback_query(AccessForm.tier, F.data.startswith("tier:"))
async def choose_tier(callback: CallbackQuery, state: FSMContext) -> None:
    tier = callback.data.split(":", 1)[1]
    await state.update_data(tier=tier)
    await state.set_state(AccessForm.scope)
    await callback.message.edit_text(f"Selected {tier}. Enter the room, project, or scope you need:")
    await callback.answer()


@dp.message(AccessForm.scope)
async def choose_scope(message: Message, state: FSMContext) -> None:
    await state.update_data(scope=message.text.strip())
    await state.set_state(AccessForm.role)
    await message.answer("What is your role or project connection? Include the expected duration if temporary.")


@dp.message(AccessForm.role)
async def finish(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    request_id = insert_access(message.from_user.id, message.from_user.username or "", data["tier"], data["scope"], message.text.strip())
    text = (f"ACCESS REQUEST #{request_id}\nUser: @{message.from_user.username or message.from_user.id}\n"
            f"Tier: {data['tier']}\nScope: {data['scope']}\nRole/project: {message.text.strip()}\n"
            "Approve only after checking the access register and review date.")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Mark reviewed", callback_data=f"review:{request_id}")]])
    await notify_admins_async(bot, text, keyboard)
    await message.answer(f"Request #{request_id} received. An owner will review it. Use /cancel to abandon future requests.")
    await state.clear()


@dp.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Request cancelled.")


@dp.callback_query(F.data.startswith("review:"))
async def review(callback: CallbackQuery) -> None:
    if callback.from_user.id not in __import__("src.common", fromlist=["admin_ids"]).admin_ids():
        await callback.answer("Admins only", show_alert=True)
        return
    await callback.answer("Record the approval/rejection in the access register, then grant access manually.", show_alert=True)


async def main() -> None:
    init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
