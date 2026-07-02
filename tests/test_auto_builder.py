import tempfile
import unittest
from datetime import date
from pathlib import Path

from auto_builder import TASKS, build, task_for


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


if __name__ == "__main__":
    unittest.main()
