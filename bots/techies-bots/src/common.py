from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Iterable

from dotenv import load_dotenv

load_dotenv()

DB_PATH = Path(os.getenv("DATABASE_PATH", "data/techies_bots.sqlite3"))
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def admin_ids() -> set[int]:
    return {int(item.strip()) for item in os.getenv("ADMIN_IDS", "").split(",") if item.strip()}


def int_list(name: str) -> list[int]:
    return [int(item.strip()) for item in os.getenv(name, "").split(",") if item.strip()]


def db() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with db() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS access_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                username TEXT,
                requested_tier TEXT NOT NULL,
                room_or_scope TEXT NOT NULL,
                role_or_project TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS pulses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                project TEXT NOT NULL,
                status TEXT NOT NULL,
                blocker TEXT NOT NULL,
                next_step TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                category TEXT NOT NULL,
                body TEXT NOT NULL,
                anonymous INTEGER NOT NULL DEFAULT 0,
                status TEXT NOT NULL DEFAULT 'received',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            """
        )


def insert_access(user_id: int, username: str, tier: str, scope: str, role: str) -> int:
    with db() as connection:
        cursor = connection.execute(
            "INSERT INTO access_requests(user_id, username, requested_tier, room_or_scope, role_or_project) VALUES (?, ?, ?, ?, ?)",
            (user_id, username, tier, scope, role),
        )
        return int(cursor.lastrowid)


def insert_pulse(user_id: int, project: str, status: str, blocker: str, next_step: str) -> int:
    with db() as connection:
        cursor = connection.execute(
            "INSERT INTO pulses(user_id, project, status, blocker, next_step) VALUES (?, ?, ?, ?, ?)",
            (user_id, project, status, blocker, next_step),
        )
        return int(cursor.lastrowid)


def insert_feedback(user_id: int, category: str, body: str, anonymous: bool) -> int:
    with db() as connection:
        cursor = connection.execute(
            "INSERT INTO feedback(user_id, category, body, anonymous) VALUES (?, ?, ?, ?)",
            (user_id, category, body, int(anonymous)),
        )
        return int(cursor.lastrowid)


def notify_admins(bot, text: str, reply_markup=None) -> None:
    # Caller awaits each send; keeping this helper sync-friendly makes the routing explicit.
    raise NotImplementedError("Use the async notify_admins_async helper")


async def notify_admins_async(bot, text: str, reply_markup=None) -> None:
    for user_id in admin_ids():
        await bot.send_message(user_id, text, reply_markup=reply_markup)
