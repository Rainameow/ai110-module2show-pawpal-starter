"""
pawpal_system.py
Core logic layer for PawPal+.
Contains Task, Pet, Owner, and Scheduler classes.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
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
        self.completed = True

        if self.frequency == "once":
            return None

        current_date = datetime.strptime(self.due_date, "%Y-%m-%d")
        if self.frequency == "daily":
            next_date = current_date + timedelta(days=1)
        elif self.frequency == "weekly":
            next_date = current_date + timedelta(weeks=1)
        else:
            return None

        return Task(
            description=self.description,
            due_time=self.due_time,
            due_date=next_date.strftime("%Y-%m-%d"),
            frequency=self.frequency,
            completed=False,
            pet_name=self.pet_name,
        )


@dataclass
class Pet:
    """Represents a pet and its list of tasks."""
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Adds a task to this pet."""
        task.pet_name = self.name
        self.tasks.append(task)

    def list_tasks(self) -> List[Task]:
        """Returns all tasks belonging to this pet."""
        return self.tasks

    def task_count(self) -> int:
        """Returns the number of tasks this pet has."""
        return len(self.tasks)


@dataclass
class Owner:
    """Represents a pet owner who manages multiple pets."""
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Adds a pet to this owner's list of pets."""
        self.pets.append(pet)

    def find_pet(self, name: str) -> Optional[Pet]:
        """Finds a pet by name."""
        for pet in self.pets:
            if pet.name == name:
                return pet
        return None

    def get_all_tasks(self) -> List[Task]:
        """Gathers every task across all of this owner's pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


class Scheduler:
    """The 'brain' of PawPal+. Organizes and manages tasks across pets."""

    def __init__(self, owner: Owner):
        self.owner = owner

    def sort_by_time(self) -> List[Task]:
        """Returns tasks sorted chronologically by due_time."""
        tasks = self.owner.get_all_tasks()
        return sorted(tasks, key=lambda t: (t.due_date, t.due_time))

    def filter_tasks(self, status: Optional[bool] = None, pet_name: Optional[str] = None) -> List[Task]:
        """Filters tasks by completion status and/or pet name."""
        tasks = self.owner.get_all_tasks()

        if pet_name is not None:
            tasks = [t for t in tasks if t.pet_name == pet_name]

        if status is not None:
            tasks = [t for t in tasks if t.completed == status]

        return tasks

    def detect_conflicts(self) -> List[str]:
        """Detects tasks scheduled at the same time and returns warnings."""
        warnings = []
        tasks = self.owner.get_all_tasks()
        seen = {}

        for task in tasks:
            key = (task.due_date, task.due_time)
            if key in seen:
                other = seen[key]
                warnings.append(
                    f"Conflict at {task.due_date} {task.due_time}: "
                    f"'{other.description}' ({other.pet_name}) overlaps with "
                    f"'{task.description}' ({task.pet_name})"
                )
            else:
                seen[key] = task

        return warnings

    def mark_task_complete(self, pet_name: str, task: Task) -> Optional[Task]:
        """Marks a task complete via its owning pet, handling recurrence."""
        pet = self.owner.find_pet(pet_name)
        if pet is None or task not in pet.tasks:
            return None

        next_task = task.mark_complete()
        if next_task is not None:
            pet.add_task(next_task)

        return next_task