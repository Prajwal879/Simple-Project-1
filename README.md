# Simple Website Uptime Checker 🌐

A beginner-friendly DevOps project that checks whether websites are reachable and reports their response time. It runs locally and is automatically tested by GitHub Actions.

This project is completely free and uses only Python's standard library—there are no packages, API keys, subscriptions, or servers to configure.

## Autonomous Daily DevOps Builder ☀️

At **9:00 AM India time every day**, a free GitHub Actions workflow chooses and implements one small DevOps utility under `completed-work/`. It tests the repository, commits the finished work directly to the default branch, and creates an assigned GitHub issue describing exactly what was completed. GitHub uses that assignment to send the morning email update.

To receive the pull-request email:

1. On GitHub, open **Settings → Actions → General → Workflow permissions** and select **Read and write permissions**.
2. Open this repository's **Watch** menu and choose **All Activity**.
3. Ensure email notifications are enabled in your GitHub notification settings.

You can test it immediately from **Actions → Autonomous Daily DevOps Builder → Run workflow**. No external email provider is used; GitHub sends its normal issue-assignment and repository notification.

## What it does

- Checks one website or several websites.
- Automatically adds `https://` when the scheme is missing.
- Shows a clear `[UP]` or `[DOWN]` result on every terminal.
- Reports response time in milliseconds.
- Returns exit code `1` when any website is down, making it useful in scripts and CI/CD pipelines.
- Runs automated tests on every GitHub push and pull request.

## Requirements

- Python 3.10 or newer
- An internet connection when checking real websites

## Run the checker

Check a single website:

```bash
python uptime_checker.py https://example.com
```

On Windows, if `python` is unavailable, use:

```powershell
py -3 uptime_checker.py https://example.com
```

Check multiple websites:

```bash
python uptime_checker.py example.com github.com
```

Or edit `sites.txt` and run the checker without arguments:

```bash
python uptime_checker.py
```

Example output:

```text
[UP]    https://example.com  184 ms  (reachable)
[UP]    https://github.com  231 ms  (reachable)
```

Set a custom timeout:

```bash
python uptime_checker.py example.com --timeout 10
```

## Run the tests

```bash
python -m unittest discover -s tests -v
```

The tests do not access the internet. They simulate successful and failed requests, so they remain fast and reliable.

## Project structure

```text
.
├── .github/workflows/test.yml   # Free GitHub Actions CI pipeline
├── tests/test_uptime_checker.py # Automated unit tests
├── uptime_checker.py            # Main checker program
├── sites.txt                    # Websites checked by default
└── README.md                    # Project instructions
```

## What was implemented

This first project introduces several basic DevOps ideas: health monitoring, useful process exit codes, configuration through a text file, automated testing, and continuous integration with GitHub Actions.

## Ideas for the next version

- Save results to a log file.
- Send a notification when a website goes down.
- Run checks on a GitHub Actions schedule.
- Display historical uptime in a small dashboard.
