"""
tests/test_pawpal.py
Basic tests verifying task completion and task addition behavior.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pawpal_system import Pet, Task


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