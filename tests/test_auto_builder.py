import tempfile
import unittest
from datetime import date
from pathlib import Path

from auto_builder import TASKS, build, next_task, task_for


class AutoBuilderTests(unittest.TestCase):
    def test_task_selection_is_stable(self):
        day = date(2026, 7, 3)
        self.assertEqual(task_for(day), task_for(day))

    def test_tasks_rotate_by_day(self):
        selected = {task_for(date(2026, 7, day))["slug"] for day in range(1, 8)}
        self.assertEqual(len(selected), len(TASKS))

    def test_build_creates_implementation_and_readme(self):
        with tempfile.TemporaryDirectory() as directory:
            output, task = build(date(2026, 7, 3), Path(directory))
            self.assertTrue((output / "README.md").exists())
            for name in task["files"]:
                self.assertTrue((output / name).exists())

    def test_next_task_skips_completed_project_type(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            completed = root / "completed-work" / f"2026-07-01-{TASKS[0]['slug']}"
            completed.mkdir(parents=True)
            self.assertEqual(next_task(root), TASKS[1])


if __name__ == "__main__":
    unittest.main()
