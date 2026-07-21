from __future__ import annotations

import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from .common import admin_ids, init_db, insert_feedback, notify_admins_async


class FeedbackForm(StatesGroup):
    category = State()
    body = State()
    anonymity = State()


bot = Bot(os.environ["FEEDBACK_TOKEN"])
dp = Dispatcher()


def category_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Suggestion", callback_data="category:suggestion")],
        [InlineKeyboardButton(text="Complaint", callback_data="category:complaint")],
        [InlineKeyboardButton(text="Safety / urgent", callback_data="category:safety")],
        [InlineKeyboardButton(text="Access issue", callback_data="category:access")],
    ])


def anonymity_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Named", callback_data="anonymous:0")],
        [InlineKeyboardButton(text="Anonymous to the community", callback_data="anonymous:1")],
    ])


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("TECHIES Feedback Router. Use /feedback to submit a suggestion, complaint, safety issue, or access issue privately.")


@dp.message(Command("feedback"))
async def feedback(message: Message, state: FSMContext) -> None:
    await state.set_state(FeedbackForm.category)
    await message.answer("Choose a category:", reply_markup=category_keyboard())


@dp.callback_query(FeedbackForm.category, F.data.startswith("category:"))
async def choose_category(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(category=callback.data.split(":", 1)[1])
    await state.set_state(FeedbackForm.body)
    await callback.message.edit_text("Describe the feedback. Do not include passwords, API keys, or unnecessary personal data.")
    await callback.answer()


@dp.message(FeedbackForm.body)
async def body(message: Message, state: FSMContext) -> None:
    await state.update_data(body=message.text.strip())
    await state.set_state(FeedbackForm.anonymity)
    await message.answer("Should this be anonymous to the wider community? Admins may still see the sender for safety and abuse handling.", reply_markup=anonymity_keyboard())


@dp.callback_query(FeedbackForm.anonymity, F.data.startswith("anonymous:"))
async def finish(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    anonymous = callback.data.endswith(":1")
    feedback_id = insert_feedback(callback.from_user.id, data["category"], data["body"], anonymous)
    sender = "anonymous to community" if anonymous else f"@{callback.from_user.username or callback.from_user.id}"
    text = (f"FEEDBACK FB-{feedback_id}\nCategory: {data['category']}\nSender: {sender}\n"
            f"Status: received\nContent:\n{data['body']}\n\nDo not repost private details.")
    await notify_admins_async(bot, text)
    await callback.message.edit_text(f"Feedback FB-{feedback_id} received. You will get a private status update if follow-up is needed.")
    await callback.answer()
    await state.clear()


@dp.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Feedback cancelled.")


async def main() -> None:
    init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
