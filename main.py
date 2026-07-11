"""
main.py
CLI demo script for PawPal+. Verifies the logic layer works before
wiring it into the Streamlit UI.
"""

from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler

TODAY = datetime.today().strftime("%Y-%m-%d")


def main():
    # Create an Owner and two Pets
    owner = Owner(name="Raina")
    dog = Pet(name="Buddy", species="Dog")
    cat = Pet(name="Whiskers", species="Cat")
    owner.add_pet(dog)
    owner.add_pet(cat)

    # Add tasks with different times
    dog.add_task(Task(description="Morning walk", due_time="08:00", due_date=TODAY))
    dog.add_task(Task(description="Evening walk", due_time="18:00", due_date=TODAY))
    cat.add_task(Task(description="Feed breakfast", due_time="08:30", due_date=TODAY))

    # Print today's schedule
    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time()

    print(f"Today's Schedule ({TODAY})")
    print("-" * 40)
    for task in sorted_tasks:
        status = "Done" if task.completed else "Pending"
        print(f"[{task.due_time}] {task.pet_name}: {task.description} ({status})")


if __name__ == "__main__":
    main()
