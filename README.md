# DSO-576 · 13-agent

A Codex starter for running a targeted quiz, carrying progress between sessions, and revising a draft.

## Run a practice round

Open this repository as the Codex workspace. Attach the course materials and any prior quiz answers you want to use. Then ask Codex to use the `targeted_quiz_workflow` agent. It coordinates diagnosis, question writing, and an independent answer check. After you attempt the quiz, it gives feedback and a progress record you can save for the next round. See the [quiz workflow guide](.agent/README.md) for a starter prompt.

## Try the AI Diary

Follow the [hook setup guide](.codex/hooks/README.md) to review and trust the three hooks in Codex. This hook implementation uses Python 3.8+ on macOS or Linux. Once enabled, finish a turn and open a new Codex session in the same repository. Ask what happened last time and what to work on next. The earlier checkpoint is recorded locally in `.codex/diary.md`.

## Revise a draft

Attach or paste your draft and ask Codex to use [`$plain-writing`](.agents/skills/plain-writing/SKILL.md) to make it more specific and concise. Include any assignment or style requirements you want to preserve.
