"""
main.py
CLI demo script for PawPal+. Verifies the logic layer works before
wiring it into the Streamlit UI.
"""

from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler

TODAY = datetime.today().strftime("%Y-%m-%d")


def main():
    owner = Owner(name="Raina")
    dog = Pet(name="Buddy", species="Dog")
    cat = Pet(name="Whiskers", species="Cat")
    owner.add_pet(dog)
    owner.add_pet(cat)

    # Tasks added out of order, including a daily recurring task
    # and a duplicate time to trigger conflict detection
    dog.add_task(Task(description="Evening walk", due_time="18:00", due_date=TODAY, frequency="daily"))
    dog.add_task(Task(description="Morning walk", due_time="08:00", due_date=TODAY, frequency="daily"))
    cat.add_task(Task(description="Feed breakfast", due_time="08:00", due_date=TODAY))  # conflicts with walk
    cat.add_task(Task(description="Vet appointment", due_time="14:30", due_date=TODAY))

    scheduler = Scheduler(owner)

    # Sorted schedule
    print(f"Today's Schedule ({TODAY})")
    print("-" * 40)
    for task in scheduler.sort_by_time():
        status = "Done" if task.completed else "Pending"
        print(f"[{task.due_time}] {task.pet_name}: {task.description} ({status})")
    print()

    # Filtering demo: incomplete tasks for Buddy only
    print("Buddy's incomplete tasks:")
    for t in scheduler.filter_tasks(status=False, pet_name="Buddy"):
        print(f"  - [{t.due_time}] {t.description}")
    print()

    # Conflict detection demo
    print("Conflict check:")
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for c in conflicts:
            print(f"  {c}")
    else:
        print("  No conflicts found.")
    print()

    # Recurrence demo: complete the morning walk, show next occurrence
    print("Marking 'Morning walk' complete...")
    morning_walk = dog.tasks[1]
    next_task = scheduler.mark_task_complete("Buddy", morning_walk)
    if next_task:
        print(f"  Next occurrence auto-scheduled: {next_task.due_date} at {next_task.due_time}")


if __name__ == "__main__":
    main()