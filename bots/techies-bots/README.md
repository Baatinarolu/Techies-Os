# TECHIES custom bot suite

This is a starter implementation for the three custom bots defined in the playbook:

1. **Access Concierge** — collects room access requests and sends approval cards to admins.
2. **Project Pulse** — collects a project status update and saves a timestamped pulse.
3. **Feedback Router** — privately accepts feedback and assigns a tracking ID.

These bots do not create Telegram groups/channels and do not contain credentials. You must create the bots in BotFather, add their tokens to a secret environment, and configure the relevant admin IDs and room IDs.

## Requirements

- Python 3.11+
- Telegram bot tokens created through BotFather
- A small always-on host (VPS, Docker host, or similar)
- SQLite for the starter deployment; use PostgreSQL before significant scale

## Local run

```bash
cd bots/techies-bots
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env; never commit it.
python -m src.concierge
```

Run `src.pulse` and `src.feedback` in separate processes with their own tokens. Each bot polls Telegram; do not run two copies of the same bot token.

## BotFather setup

Create three bots and set commands similar to:

- Concierge: `/start`, `/request_access`, `/cancel`
- Pulse: `/start`, `/pulse`, `/cancel`
- Feedback: `/start`, `/feedback`, `/cancel`

Keep group privacy mode enabled unless a bot genuinely needs to read all messages. Prefer private conversations and explicit commands.

## Security checklist

- [ ] Tokens stored in a secret manager or host environment, never in Git.
- [ ] `ADMIN_IDS` contains only trusted numeric Telegram user IDs.
- [ ] Concierge is the only bot that can send access requests to admins.
- [ ] No bot is given Tier 4 room access by default.
- [ ] Test with fake data and a non-admin account.
- [ ] Add rate limiting and PostgreSQL before public scale.
- [ ] Back up `data/techies_bots.sqlite3` and keep an export of decisions outside Telegram.
