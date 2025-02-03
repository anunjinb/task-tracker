import argparse
import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

def load_tasks():
    # Check if the file exists and is not empty
    if os.path.exists('tasks.json') and os.path.getsize('tasks.json') > 0:
        with open('tasks.json', 'r') as f:
            return json.load(f)
    else:
        # If the file doesn't exist or is empty, return an empty list
        return []

def save_tasks(tasks):
    with open('task.json', "w") as f:
        json.dump(tasks, f, indent=4)

def main():
    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    parser.add_argument("command", choices=["add", "update", "delete", "list", "mark-in-progress", "mark-done"],
                        help="Command to execute")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="Arguments for the command")

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.args)
    elif args.command == "update":
        update_task(args.args)
    elif args.command == "delete":
        delete_task(args.args)
    elif args.command == "list":
        list_tasks(args.args)
    elif args.command == "mark-in-progress":
        mark_in_progress(args.args)
    elif args.command == "mark-done":
        mark_done(args.args)

def add_task(args):
    description = " ".join(args)
    tasks = load_tasks()
    task_id = len(tasks) + 1
    task = {
        "id": task_id,
        "description": description,
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat(),
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {task_id})")


def update_task(args):
    task_id = int(args[0])
    new_description = " ".join(args[1:])
    tasks = load_tasks()
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task:
        task["description"] = new_description
        task["updatedAt"] = datetime.now().isoformat()
        save_tasks(tasks)
        print(f"Task {task_id} updated successfully")
    else:
        print(f"Task with ID {task_id} not found")

def delete_task(args):
    task_id = int(args[0])
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)
    print(f"Task {task_id} deleted successfully")


def list_tasks(args):
    status = args[0] if args else None
    tasks = load_tasks()
    filtered_tasks = [task for task in tasks if status is None or task["status"] == status]
    for task in filtered_tasks:
        print(f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}")

def mark_in_progress(args):
    task_id = int(args[0])
    tasks = load_tasks()
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task:
        task["status"] = "in-progress"
        task["updatedAt"] = datetime.now().isoformat()
        save_tasks(tasks)
        print(f"Task {task_id} marked as in progress")
    else:
        print(f"Task with ID {task_id} not found")


def mark_done(args):
    task_id = int(args[0])
    tasks = load_tasks()
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task:
        task["status"] = "done"
        task["updatedAt"] = datetime.now().isoformat()
        save_tasks(tasks)
        print(f"Task {task_id} marked as done")
    else:
        print(f"Task with ID {task_id} not found")


if __name__ == "__main__":
    main()
