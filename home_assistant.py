import streamlit as st
import pandas as pd
import json
from pathlib import Path
from datetime import date

st.set_page_config(
    page_title="AI Home Assistant",
    page_icon="🏠",
    layout="wide"
)

DATA_FILE = Path(__file__).with_name("home_tasks.json")

def load_tasks():
    if DATA_FILE.exists():
        try:
            data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            st.warning("Could not load saved tasks. Starting with an empty list.")
    return []

def save_tasks(tasks):
    DATA_FILE.write_text(
        json.dumps(tasks, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

if "home_tasks" not in st.session_state:
    st.session_state.home_tasks = load_tasks()

st.title("🏠 AI Home Assistant")
st.write("Organise household tasks, due dates, and completion status.")

with st.form("add_task", clear_on_submit=True):
    st.subheader("Add a household task")

    col1, col2 = st.columns(2)

    with col1:
        task_name = st.text_input(
            "Task",
            placeholder="e.g. Buy groceries"
        )
        category = st.selectbox(
            "Category",
            [
                "Cleaning", "Shopping", "Cooking",
                "Maintenance", "Bills", "Other"
            ]
        )

    with col2:
        assigned_to = st.text_input(
            "Assigned to",
            placeholder="e.g. Me"
        )
        due_date = st.date_input("Due date", value=date.today())

    priority = st.selectbox("Priority", ["Low", "Medium", "High"])
    submitted = st.form_submit_button("Add Task")

    if submitted:
        if not task_name.strip():
            st.warning("Please enter a task.")
        else:
            st.session_state.home_tasks.append({
                "Task": task_name.strip(),
                "Category": category,
                "Assigned To": assigned_to.strip() or "Unassigned",
                "Due Date": due_date.isoformat(),
                "Priority": priority,
                "Completed": False
            })
            save_tasks(st.session_state.home_tasks)
            st.success("Task added successfully.")

tasks = st.session_state.home_tasks

st.divider()
st.subheader("Household Dashboard")

if not tasks:
    st.info("No tasks yet. Add your first household task above.")
else:
    df = pd.DataFrame(tasks)
    total = len(df)
    completed = int(df["Completed"].sum())
    pending = total - completed

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Tasks", total)
    c2.metric("Completed", completed)
    c3.metric("Pending", pending)

    st.progress(completed / total)

    st.subheader("Your Tasks")

    for i, task in enumerate(tasks):
        with st.container(border=True):
            col1, col2 = st.columns([4, 1])

            with col1:
                st.markdown(f"**{task['Task']}**")
                st.caption(
                    f"{task['Category']} · "
                    f"Assigned to: {task['Assigned To']} · "
                    f"Due: {task['Due Date']} · "
                    f"Priority: {task['Priority']}"
                )

            with col2:
                new_status = st.checkbox(
                    "Completed",
                    value=bool(task["Completed"]),
                    key=f"task_done_{i}"
                )

                if new_status != bool(task["Completed"]):
                    task["Completed"] = new_status
                    save_tasks(tasks)
                    st.rerun()

    st.subheader("Manage Tasks")

    task_options = [
        f"{i + 1}. {task['Task']}" for i, task in enumerate(tasks)
    ]
    selected = st.selectbox("Select a task to delete", task_options)

    if st.button("Delete Selected Task"):
        index = task_options.index(selected)
        tasks.pop(index)
        save_tasks(tasks)
        st.rerun()

    csv_data = pd.DataFrame(tasks).to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Task List (CSV)",
        data=csv_data,
        file_name="home_tasks.csv",
        mime="text/csv"
    )

    if st.button("Clear All Tasks"):
        st.session_state.home_tasks = []
        save_tasks([])
        st.rerun()
