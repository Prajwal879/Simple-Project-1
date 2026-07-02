#!/usr/bin/env python3
"""Create today's small DevOps learning task using only local templates."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path


TASKS = [
    {
        "title": "Check disk usage",
        "goal": "Learn how to spot a server that is running out of storage.",
        "steps": ["Run `df -h`.", "Find the filesystem with the highest usage.", "Write down what could be safely cleaned."],
        "done": "You can identify the used percentage and available space on the busiest filesystem.",
    },
    {
        "title": "Inspect running processes",
        "goal": "Understand which processes are consuming CPU and memory.",
        "steps": ["Run `ps aux`.", "Sort or inspect the CPU and memory columns.", "Identify the top three processes."],
        "done": "You can name the processes using the most CPU or memory.",
    },
    {
        "title": "Read recent system logs",
        "goal": "Practice finding useful information in system logs.",
        "steps": ["Run `journalctl -n 20` on Linux.", "Look for warning or error messages.", "Summarize one log entry in plain language."],
        "done": "You can explain what one recent log entry means.",
    },
    {
        "title": "Check a website from the terminal",
        "goal": "Learn how an engineer quickly inspects an HTTP response.",
        "steps": ["Run `curl -I https://example.com`.", "Find the HTTP status code.", "Find one response header and explain it."],
        "done": "You understand the status code and at least one returned header.",
    },
    {
        "title": "Explore Git history",
        "goal": "Become comfortable reading a project's change history.",
        "steps": ["Run `git log --oneline -5`.", "Choose one commit.", "Run `git show <commit>` and inspect its change."],
        "done": "You can explain what the selected commit changed.",
    },
    {
        "title": "Inspect a Docker image",
        "goal": "Learn what metadata is stored in a container image.",
        "steps": ["Run `docker pull hello-world`.", "Run `docker image inspect hello-world`.", "Find its creation date and architecture."],
        "done": "You can locate basic metadata for a Docker image.",
    },
    {
        "title": "Practice environment variables",
        "goal": "Understand how applications receive configuration.",
        "steps": ["Create an environment variable named `APP_ENV`.", "Print it in the terminal.", "Read it from a tiny Python or shell script."],
        "done": "Your script reads configuration without hard-coding it.",
    },
    {
        "title": "Test DNS resolution",
        "goal": "Understand how a domain name becomes an IP address.",
        "steps": ["Run `nslookup github.com`.", "Find one returned IP address.", "Write down which DNS server answered."],
        "done": "You can identify the resolved address and responding DNS server.",
    },
    {
        "title": "Create a basic health check",
        "goal": "Practice turning a service check into a useful exit code.",
        "steps": ["Run the repository's uptime checker.", "Print the command's exit code.", "Try one invalid address and compare results."],
        "done": "You can explain why exit codes matter to CI/CD and monitoring.",
    },
    {
        "title": "Review a GitHub Actions run",
        "goal": "Learn to read the result of a CI pipeline.",
        "steps": ["Open this repository's Actions tab.", "Select the newest workflow run.", "Identify each step and whether it succeeded."],
        "done": "You can locate a failed step and its logs in GitHub Actions.",
    },
]


def task_for(day: date) -> dict:
    """Select a stable task for a date, rotating through the catalog."""
    return TASKS[day.toordinal() % len(TASKS)]


def render(day: date, task: dict) -> str:
    steps = "\n".join(f"{number}. {step}" for number, step in enumerate(task["steps"], 1))
    return f"""# Daily DevOps Task — {day.isoformat()}

## {task['title']}

**Today's goal:** {task['goal']}

### Small steps

{steps}

### Done when

{task['done']}

### Learning note

After completing the task, edit this section with two or three sentences about what you learned. Then merge the pull request.

---

Generated automatically by the free Daily DevOps Coach.
"""


def create_daily_task(day: date, root: Path) -> tuple[Path, dict]:
    task = task_for(day)
    output = root / "daily-tasks" / f"{day.isoformat()}.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(day, task), encoding="utf-8", newline="\n")
    return output, task


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", type=date.fromisoformat, default=date.today(), help="date in YYYY-MM-DD format")
    parser.add_argument("--output-root", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    output, task = create_daily_task(args.date, args.output_root)
    print(f"TASK_DATE={args.date.isoformat()}")
    print(f"TASK_TITLE={task['title']}")
    print(f"TASK_FILE={output.relative_to(args.output_root).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
