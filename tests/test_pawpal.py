"""
tests/test_pawpal.py
Tests verifying core behaviors: task completion, task addition,
sorting, recurrence, and conflict detection.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pawpal_system import Owner, Pet, Task, Scheduler


def test_task_completion():
    """Verify mark_complete() actually changes the task's status."""
    task = Task(description="Feed", due_time="09:00", due_date="2026-07-12")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_task_addition_increases_count():
    """Verify adding a task to a Pet increases that pet's task count."""
    pet = Pet(name="Rex", species="Dog")
    assert pet.task_count() == 0
    pet.add_task(Task(description="Walk", due_time="08:00", due_date="2026-07-12"))
    assert pet.task_count() == 1


def test_sorting_correctness():
    """Verify tasks are returned in chronological order."""
    owner = Owner(name="TestOwner")
    pet = Pet(name="Rex", species="Dog")
    owner.add_pet(pet)

    pet.add_task(Task(description="Dinner", due_time="18:00", due_date="2026-07-12"))
    pet.add_task(Task(description="Breakfast", due_time="07:00", due_date="2026-07-12"))
    pet.add_task(Task(description="Lunch", due_time="12:00", due_date="2026-07-12"))

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time()
    times = [t.due_time for t in sorted_tasks]

    assert times == ["07:00", "12:00", "18:00"]


def test_recurrence_creates_next_day_task():
    """Confirm marking a daily task complete creates a new task for the next day."""
    owner = Owner(name="TestOwner")
    pet = Pet(name="Rex", species="Dog")
    owner.add_pet(pet)

    daily_task = Task(description="Walk", due_time="08:00", due_date="2026-07-12", frequency="daily")
    pet.add_task(daily_task)

    scheduler = Scheduler(owner)
    next_task = scheduler.mark_task_complete("Rex", daily_task)

    assert daily_task.completed is True
    assert next_task is not None
    assert next_task.due_date == "2026-07-13"
    assert next_task.completed is False
    assert next_task in pet.tasks


def test_conflict_detection_flags_duplicate_times():
    """Verify the Scheduler flags two tasks scheduled at the same date/time."""
    owner = Owner(name="TestOwner")
    pet = Pet(name="Rex", species="Dog")
    owner.add_pet(pet)

    pet.add_task(Task(description="Walk", due_time="08:00", due_date="2026-07-12"))
    pet.add_task(Task(description="Feed", due_time="08:00", due_date="2026-07-12"))

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1