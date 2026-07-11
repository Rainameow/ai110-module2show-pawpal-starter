"""
pawpal_system.py
Core logic layer for PawPal+.
Contains Task, Pet, Owner, and Scheduler classes.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Task:
    """Represents a single pet-care activity."""
    description: str
    due_time: str
    due_date: str
    frequency: str = "once"
    completed: bool = False
    pet_name: str = ""

    def mark_complete(self) -> Optional["Task"]:
        """Marks this task complete and returns the next occurrence if recurring."""
        pass


@dataclass
class Pet:
    """Represents a pet and its list of tasks."""
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Adds a task to this pet."""
        pass

    def list_tasks(self) -> List[Task]:
        """Returns all tasks belonging to this pet."""
        pass

    def task_count(self) -> int:
        """Returns the number of tasks this pet has."""
        pass


@dataclass
class Owner:
    """Represents a pet owner who manages multiple pets."""
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Adds a pet to this owner's list of pets."""
        pass

    def find_pet(self, name: str) -> Optional[Pet]:
        """Finds a pet by name."""
        pass

    def get_all_tasks(self) -> List[Task]:
        """Gathers every task across all of this owner's pets."""
        pass


class Scheduler:
    """The 'brain' of PawPal+. Organizes and manages tasks across pets."""

    def __init__(self, owner: Owner):
        self.owner = owner

    def sort_by_time(self) -> List[Task]:
        """Returns tasks sorted chronologically by due_time."""
        pass

    def filter_tasks(self, status: Optional[bool] = None, pet_name: Optional[str] = None) -> List[Task]:
        """Filters tasks by completion status and/or pet name."""
        pass

    def detect_conflicts(self) -> List[str]:
        """Detects tasks scheduled at the same time and returns warnings."""
        pass

    def mark_task_complete(self, pet_name: str, task: Task) -> Optional[Task]:
        """Marks a task complete via its owning pet, handling recurrence."""
        pass
