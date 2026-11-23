"""Exercise the diary handlers in disposable projects with native hook payloads."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "ai_diary.py"


class DiaryTest(unittest.TestCase):
    def exercise(self, root, with_git):
        script = root / ".codex/hooks/ai_diary.py"
        script.parent.mkdir(parents=True)
        shutil.copyfile(SOURCE, script)
        project_file = root / "example.py"
        project_file.write_text('VALUE = 1\n', encoding="utf-8")
        prior_file = root / "preexisting.py"
        prior_file.write_text('VALUE = 4\n', encoding="utf-8")
        if with_git:
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            subprocess.run(["git", "-C", str(root), "add", "example.py"], check=True)

        diary = root / ".codex/diary.md"
        log = root.parent / "transcript.jsonl"
        report = "Completed work: Updated example.py.\nNext steps: Add a validation test."
        events = [
            {"type": "event_msg", "payload": {"type": "exec_command_end", "exit_code": 7}},
            {"type": "event_msg", "payload": {"type": "task_complete", "last_agent_message": report}},
        ]

        def hook(event, session="first", **extras):
            payload = {"hook_event_name": event, "cwd": str(root), "session_id": session,
                       "transcript_path": str(log), **extras}
            result = subprocess.run([sys.executable, str(script)], input=json.dumps(payload),
                                    text=True, capture_output=True, cwd=root, check=True)
            self.assertEqual(result.stderr, "")
            return json.loads(result.stdout)

        self.assertEqual(hook("SessionStart", source="startup"), {})
        project_file.write_text('VALUE = 2\n', encoding="utf-8")
        log.write_text("".join(json.dumps(row) + "\n" for row in events), encoding="utf-8")
        self.assertEqual(hook("Stop", last_assistant_message=report, stop_hook_active=True), {})
        checkpoint = diary.read_text()
        self.assertIn("Stop checkpoint", checkpoint)
        self.assertIn("Modified `example.py`", checkpoint)
        self.assertNotIn("preexisting.py", checkpoint)
        self.assertIn("exited with status 7", checkpoint)
        self.assertIn("Add a validation test.", checkpoint)
        self.assertEqual(hook("Stop", last_assistant_message=report), {})
        self.assertEqual(checkpoint, diary.read_text())

        checkpoint_context = hook("SessionStart", "second", source="startup")["hookSpecificOutput"]
        self.assertEqual(checkpoint_context["hookEventName"], "SessionStart")
        self.assertIn("Add a validation test.", checkpoint_context["additionalContext"])
        self.assertIn("Modified `example.py`", checkpoint_context["additionalContext"])

        self.assertEqual(hook("SessionEnd", reason="other"), {})
        finished = diary.read_text()
        self.assertEqual(finished.count("<!-- ai-diary:first -->"), 1)
        self.assertIn("Session ended", finished)
        self.assertIn("Add a validation test.", finished)
        self.assertIn("Git tracked" if with_git else "Git inventory unavailable", finished)
        self.assertEqual(hook("SessionEnd", reason="other"), {})
        self.assertEqual(finished, diary.read_text())
        self.assertEqual(hook("SessionStart", source="resume"), {})

    def test_git_and_plain_folder(self):
        for with_git in (False, True):
            with self.subTest(with_git=with_git), tempfile.TemporaryDirectory() as folder:
                root = Path(folder) / "project"
                self.exercise(root, with_git)


if __name__ == "__main__":
    unittest.main()
