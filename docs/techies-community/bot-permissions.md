# Bot installation and least-privilege checklist

Bots are optional. Verify the handle, availability, privacy policy, and current permissions in Telegram before installation. Keep canonical records outside Telegram.

| Bot | Candidate rooms | Minimum useful permission | Owner |
|---|---|---|---|
| ControllerBot `@ControllerBot` | Announcements, Resource Library, Marketing & Growth, Showcase, Knowledge Base | Post/edit scheduled channel content only | |
| Combot `@combot` | Lounge, Idea Lab, AI Lab, Collaboration Hub, Cybersecurity | Delete spam, warn/mute; avoid ban rights unless necessary | |
| Rose `@MissRose_bot` | Lounge, Help Desk, Community Feedback | Filters, warnings, anti-spam; avoid broad content access if not needed | |
| Trello bot `@trello_bot` | Task Center, Project Follow-Up | Link/create cards only in the selected board | |
| GitHub bot `@githubbot` | Software Development | Read-only notifications; no repository write access | |
| QuizBot `@QuizBot` | Learning Hub | Post quizzes; no moderation rights | |
| VoteBot `@vote` | Polls & Decisions | Create/post polls; no room moderation rights | |
| Skeddy `@SkeddyBot` | Personal event reminders | Personal opt-in reminders; do not use as calendar source of truth | |

## Installation controls

- [ ] Bot purpose and owner recorded.
- [ ] Only required room(s) added.
- [ ] Admin rights reviewed one by one.
- [ ] Ban/delete/pin rights removed unless essential.
- [ ] No production secrets, tokens, HR data, financial data, or private client data shared with a bot.
- [ ] Manual fallback documented.
- [ ] Bot access reviewed monthly and after an owner leaves.
- [ ] Bot removed immediately if behavior changes or the handle cannot be verified.
