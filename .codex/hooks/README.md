# AI Diary

AI Diary runs under Codex's native project hooks. It uses Python 3.8+ on macOS
or Linux. Git is optional. The hooks use local files and do not call an AI
service. The diary and its working state are ignored by Git and created locally by the hooks.

## Activate

1. Start a new Codex CLI session from the project root. Trust the project when
   prompted. In the Codex desktop app, open the project as a local workspace.
2. In the CLI, run `/hooks`. Review and trust the three project hooks. Leave
   hooks enabled in Codex settings. Start another fresh session so the
   trusted startup hook runs before its first turn.
3. After a turn completes, open `.codex/diary.md` to see its checkpoint. The
   same entry is finalized on normal session shutdown. Leaving a desktop
   chat open or switching chats can delay shutdown.

For this folder, use the project root as the working directory. In a Git
checkout, the command resolves the script relative to the Git root, including
when Codex starts from a subdirectory. CLI automation outside Git requires
`codex exec --skip-git-repo-check`. For hook trust, event timing, and output
formats, see [the official OpenAI documentation](https://learn.chatgpt.com/docs/hooks).

## Test

Run `python3 .codex/hooks/test_ai_diary.py` from the project root. The test uses
disposable projects with and without Git. It checks an actual Python change,
an existing file, a logged shell failure, checkpoint retry, finalization retry,
and the context payload delivered by the next startup handler.

For an interactive test, use a fresh trusted session and ask Codex to create
a new scratch Python file and report its work under **Completed work**,
**Unfinished tasks**, and **Next steps**. Choose a filename that does not
already exist. End that session and open a different one. Ask “What happened
last time, and what should I work on next?” The diary excerpt is available
before the first turn. Compare the answer with the most recent entry, then
remove the scratch file when finished.

## Evidence and limits

- Startup records file fingerprints. Checkpoints compare them with the current
  working tree. Git limits that inventory to tracked and unignored files. In
  a plain folder the hook scans the project tree, excluding common caches,
  dependency directories, and its own generated files. A file change can come
  from Codex, the user, or another process in the same checkout.
- If present, the hook reads up to the last 1 MiB of Codex's local transcript.
  It recognizes structured patch results, shell exit codes, interrupted turns,
  errors, and the latest structured Codex plan. It also looks for handoff
  headings in the final assistant report. Plan items and report excerpts are
  attributed to Codex. Their content can be incomplete or mistaken. Keep
  sensitive information out of handoff notes. No raw tool output, tool commands,
  user prompts, or file contents are saved in the diary.
- The diary captures net file changes. Temporary edits reversed before a
  checkpoint, index-only changes, activity beyond the transcript window,
  unlogged actions, and missing transcripts can leave gaps. Large or unreadable
  files and timed-out scans can make a comparison partial.
- Stop saves after a turn reaches its normal stopping point. A crash during a
  turn can leave only the preceding checkpoint. An existing session opened before
  activation can lack a startup baseline. The report calls out missing evidence.
- Each session has one entry. Startup injects only the latest entry from another
  session, shortened to roughly 3,600 characters when needed. Disk history stays
  in the diary. Local baselines accumulate in `.codex/diary-state/`. Keep that
  directory and the diary private if you put this folder under version control.
