# TECHIES COMMUNITY — Telegram Build Pack

This folder contains the practical setup files for implementing the TECHIES COMMUNITY Telegram architecture.

## Naming standard

**Option B — Clean workspace:** visible names use an emoji plus the room name; public handles use the `techies_...` namespace.

Example: `📢 Announcements` → `https://t.me/techies_announcements`

> Replace placeholder handles with the actual Telegram links after rooms are created. Never put private Tier 3/4 invite links in a public directory.

## Build order

1. Complete `setup-checklist.md`.
2. Create rooms in the order in `room-registry.csv`.
3. Copy the relevant pinned message from `templates/pinned-messages.md`.
4. Configure only the bots listed in `bot-permissions.md`.
5. Track access using `operations/access-register-template.csv`.
6. Run the onboarding test using a non-admin account.

## Files

- `setup-checklist.md` — phased Telegram creation checklist.
- `room-registry.csv` — source of truth for all 28 rooms.
- `templates/pinned-messages.md` — copy-ready room pins, rules, directory, and Founder’s Office guidance.
- `operations/access-register-template.csv` — dynamic access register with no personal data prefilled.
- `operations/workflows.md` — operating procedures for onboarding, tasks, milestones, feedback, and events.
- `bot-permissions.md` — least-privilege bot installation checklist.
