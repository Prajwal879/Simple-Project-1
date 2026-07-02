import tempfile
import unittest
from datetime import date
from pathlib import Path

from daily_task import TASKS, create_daily_task, render, task_for


class DailyTaskTests(unittest.TestCase):
    def test_same_date_selects_same_task(self):
        day = date(2026, 7, 2)
        self.assertEqual(task_for(day), task_for(day))

    def test_catalog_rotates(self):
        selected = {task_for(date(2026, 7, day))["title"] for day in range(1, 11)}
        self.assertEqual(len(selected), len(TASKS))

    def test_render_contains_title_and_steps(self):
        day = date(2026, 7, 2)
        content = render(day, TASKS[0])
        self.assertIn(TASKS[0]["title"], content)
        self.assertIn("### Small steps", content)

    def test_create_writes_dated_markdown(self):
        with tempfile.TemporaryDirectory() as directory:
            output, _ = create_daily_task(date(2026, 7, 2), Path(directory))
            self.assertEqual(output.name, "2026-07-02.md")
            self.assertTrue(output.exists())


if __name__ == "__main__":
    unittest.main()
