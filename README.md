# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. This app tracks tasks (walks, feeding, meds, appointments) across multiple pets, detects scheduling conflicts, and automatically schedules the next occurrence of recurring tasks.

## System Overview

PawPal+ is built around four classes:

- **`Task`** — a single pet-care activity with a description, due time/date, frequency (once/daily/weekly), and completion status.
- **`Pet`** — holds identifying info (name, species) and its own list of tasks.
- **`Owner`** — manages multiple pets and can pull every task across all of them.
- **`Scheduler`** — the "brain" of the app; sorts tasks, filters them, detects conflicts, and handles marking tasks complete (including generating recurring tasks).

## Features

- **Multi-pet task tracking** — manage tasks across any number of pets under one owner
- **Sorting by time** — view the full schedule in chronological order
- **Filtering** — narrow tasks down by pet or by completion status
- **Conflict warnings** — get flagged when two tasks land on the same date and time
- **Daily/weekly recurrence** — completing a recurring task automatically schedules its next occurrence

## Getting started

### Setup

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Running the CLI demo

```bash
python3 main.py
```

### Running the Streamlit app

```bash
streamlit run app.py
```

## 🖥️ Sample Output

```
Today's Schedule (2026-07-12)
----------------------------------------
[08:00] Buddy: Morning walk (Pending)
[08:00] Whiskers: Feed breakfast (Pending)
[14:30] Whiskers: Vet appointment (Pending)
[18:00] Buddy: Evening walk (Pending)

Buddy's incomplete tasks:
  - [18:00] Evening walk
  - [08:00] Morning walk

Conflict check:
  Conflict at 2026-07-12 08:00: 'Morning walk' (Buddy) overlaps with 'Feed breakfast' (Whiskers)

Marking 'Morning walk' complete...
  Next occurrence auto-scheduled: 2026-07-13 at 08:00
```

## 🧪 Testing PawPal+

Run the test suite with:

```bash
python -m pytest
```

The tests cover:
- **Task completion** — verifies `mark_complete()` correctly updates a task's status
- **Task addition** — verifies adding a task increases a pet's task count
- **Sorting correctness** — verifies tasks are returned in chronological order regardless of the order they were added
- **Recurrence logic** — verifies that completing a daily task automatically schedules the next occurrence for the following day
- **Conflict detection** — verifies the Scheduler correctly flags two tasks scheduled at the same date and time

Sample test output:

```
============= test session starts ==============
platform darwin -- Python 3.13.13, pytest-9.0.3, pluggy-1.6.0
rootdir: /Users/rainamariyam/Desktop/pawpal-repo
plugins: anyio-4.13.0
collected 5 items                              

tests/test_pawpal.py .....               [100%]

============== 5 passed in 0.03s ===============
```

**Confidence Level:** ⭐⭐⭐⭐☆ (4/5) — all core behaviors are verified, but edge cases like overlapping durations (rather than exact time matches) or malformed time strings aren't yet covered.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts all tasks across every pet chronologically by date and time |
| Filtering | `Scheduler.filter_tasks(status, pet_name)` | Filters by completion status and/or a specific pet |
| Conflict handling | `Scheduler.detect_conflicts()` | Flags any two tasks (across any pets) scheduled at the exact same date and time |
| Recurring tasks | `Task.mark_complete()` | Automatically generates the next occurrence (using `timedelta`) when a daily/weekly task is completed |

## 📸 Demo Walkthrough

1. Open the app with `streamlit run app.py`.
2. In the sidebar, add a pet by entering its name and species.
3. Still in the sidebar, add a task for that pet — description, due time, and frequency (once/daily/weekly).
4. The main area shows a live, sorted schedule table across all pets.
5. If two tasks land on the same date and time, a warning banner appears at the top flagging the conflict.
6. Use the filter dropdowns to view tasks by pet or by completion status.
7. Select a task and click "Mark Complete" — if it's recurring, the next occurrence is automatically scheduled and shown.