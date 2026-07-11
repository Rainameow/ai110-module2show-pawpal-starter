"""
app.py
Streamlit UI for PawPal+. Wires the pawpal_system.py logic layer
(Owner, Pet, Task, Scheduler) into an interactive web app.
"""

import streamlit as st
from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

TODAY = datetime.today().strftime("%Y-%m-%d")

# ---------------------------------------------------------------
# Session state: create the Owner ONCE and keep it alive across
# reruns. Streamlit reruns this whole script on every interaction,
# so without this the Owner would reset every click.
# ---------------------------------------------------------------
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="My Household")

owner = st.session_state.owner
scheduler = Scheduler(owner)

st.title("🐾 PawPal+")
st.caption("Smart pet care scheduling")

# ---------------------------------------------------------------
# Sidebar: Add a Pet
# ---------------------------------------------------------------
with st.sidebar:
    st.header("Add a Pet")
    with st.form("add_pet_form", clear_on_submit=True):
        pet_name = st.text_input("Pet name")
        species = st.text_input("Species (e.g., Dog, Cat)")
        submitted_pet = st.form_submit_button("Add Pet")

        if submitted_pet:
            if pet_name.strip() and species.strip():
                owner.add_pet(Pet(name=pet_name.strip(), species=species.strip()))
                st.success(f"Added {pet_name}!")
            else:
                st.error("Please enter both a name and a species.")

    st.divider()
    st.header("Add a Task")

    if not owner.pets:
        st.info("Add a pet first to schedule tasks.")
    else:
        with st.form("add_task_form", clear_on_submit=True):
            task_pet = st.selectbox("Pet", options=[p.name for p in owner.pets])
            description = st.text_input("Task description")
            due_time = st.time_input("Due time")
            frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
            submitted_task = st.form_submit_button("Add Task")

            if submitted_task:
                if description.strip():
                    pet = owner.find_pet(task_pet)
                    pet.add_task(
                        Task(
                            description=description.strip(),
                            due_time=due_time.strftime("%H:%M"),
                            due_date=TODAY,
                            frequency=frequency,
                        )
                    )
                    st.success(f"Added '{description}' for {task_pet}.")
                else:
                    st.error("Please enter a task description.")

# ---------------------------------------------------------------
# Main area: Today's Schedule, Filters, Conflicts
# ---------------------------------------------------------------
if not owner.pets:
    st.info("👋 Welcome! Use the sidebar to add your first pet and task.")
else:
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for c in conflicts:
            st.warning(c)

    st.subheader("📅 Schedule")
    all_tasks = scheduler.sort_by_time()

    if not all_tasks:
        st.write("No tasks yet.")
    else:
        table_rows = [
            {
                "Pet": t.pet_name,
                "Time": t.due_time,
                "Task": t.description,
                "Frequency": t.frequency,
                "Status": "✅ Done" if t.completed else "⏳ Pending",
            }
            for t in all_tasks
        ]
        st.table(table_rows)

    st.divider()
    st.subheader("🔍 Filter Tasks")

    col1, col2 = st.columns(2)
    with col1:
        filter_pet = st.selectbox("By pet", options=["All"] + [p.name for p in owner.pets])
    with col2:
        filter_status = st.selectbox("By status", options=["All", "Pending", "Completed"])

    status_map = {"All": None, "Pending": False, "Completed": True}
    filtered = scheduler.filter_tasks(
        status=status_map[filter_status],
        pet_name=None if filter_pet == "All" else filter_pet,
    )

    if filtered:
        for t in filtered:
            st.write(f"[{t.due_time}] {t.pet_name}: {t.description}")
    else:
        st.write("No tasks match that filter.")

    st.divider()
    st.subheader("✅ Mark a Task Complete")

    incomplete = [t for t in all_tasks if not t.completed]
    if incomplete:
        task_labels = [f"{t.pet_name}: {t.description} ({t.due_time})" for t in incomplete]
        chosen_label = st.selectbox("Choose a task", options=task_labels)
        chosen_task = incomplete[task_labels.index(chosen_label)]

        if st.button("Mark Complete"):
            next_task = scheduler.mark_task_complete(chosen_task.pet_name, chosen_task)
            if next_task:
                st.success(f"Done! Next occurrence scheduled for {next_task.due_date}.")
            else:
                st.success("Done!")
            st.rerun()
    else:
        st.write("Everything is done! 🎉")