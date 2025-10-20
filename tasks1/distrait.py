import json
import os
import datetime
import sys
from typing import List, Dict, Any

# Define the file where tasks will be stored
TASKS_FILE = "distrait_data.json" # Renamed the data file to match the new name

def load_tasks() -> List[Dict[str, Any]]:
    """Loads tasks from the JSON file. Returns an empty list if the file is new or invalid."""
    if not os.path.exists(TASKS_FILE):
        return []
    
    try:
        with open(TASKS_FILE, 'r') as f:
            content = f.read()
            if not content:
                return []
            return json.loads(content)
    except (json.JSONDecodeError, Exception):
        # A safer failure mode is to discard corrupted data and start fresh
        print("Warning: Distrait data file is corrupted or unreadable. Starting with a clean slate.")
        return []

def save_tasks(tasks: List[Dict[str, Any]]):
    """Saves the current list of tasks to the JSON file."""
    try:
        with open(TASKS_FILE, 'w') as f:
            json.dump(tasks, f, indent=4)
    except Exception as e:
        print(f"Error saving tasks to {TASKS_FILE}: {e}")

def add_task(tasks: List[Dict[str, Any]], task_title: str):
    """Adds a task with the provided title to the list."""
    task_title = task_title.strip()
    
    if not task_title:
        print("Error: Task title cannot be empty.")
        return

    # Find the maximum existing ID and increment it, or start at 1
    max_id = max((t['id'] for t in tasks), default=0)
    task_id = max_id + 1
    
    new_task = {
        "id": task_id,
        "title": task_title,
        "status": "pending",
        "created_at": datetime.datetime.now().isoformat()
    }
    
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"\n✅ Task '{task_title}' (ID: {task_id}) added successfully to Distrait.")

def display_tasks(tasks: List[Dict[str, Any]], title: str):
    """Helper function to display a list of tasks."""
    if not tasks:
        print(f"\nNo tasks found in the {title.lower()} list.")
        return

    print(f"\n--- Distrait: {title} ---")
    
    for task in tasks:
        # Using ANSI escape codes for simple color
        status_symbol = "✅" if task['status'] == 'complete' else "⏳"
        status_color = "\033[92m" if task['status'] == 'complete' else "\033[93m"
        reset_color = "\033[0m"

        print(
            f"[{task['id']}] "
            f"{status_color}{status_symbol} {task['title']}{reset_color}"
        )
    print("-" * (len(title) + 19))

def list_tasks(tasks: List[Dict[str, Any]]):
    """Displays all tasks."""
    display_tasks(tasks, "ALL Tasks")

def search_tasks(tasks: List[Dict[str, Any]], keyword: str):
    """Searches for tasks containing the keyword in their title."""
    keyword_lower = keyword.lower()
    
    # Filter the task list based on the keyword
    matching_tasks = [
        task for task in tasks 
        if keyword_lower in task['title'].lower()
    ]
    
    display_tasks(matching_tasks, f"Search Results for '{keyword}'")


def print_usage():
    """Prints the command usage instructions using the new file name."""
    print("\n--- Distrait CLI Usage ---")
    print(f"File: {os.path.basename(__file__)}")
    print("To add a task:")
    print(f"  python3 {sys.argv[0]} add \"Your task title here\"")
    print("To list ALL tasks:")
    print(f"  python3 {sys.argv[0]} list")
    print("To search for a task:")
    print(f"  python3 {sys.argv[0]} search keyword")
    print("--------------------------\n")


def main():
    """Handles command-line arguments and dispatches actions."""
    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1].lower()
    tasks = load_tasks()

    if command == 'add':
        if len(sys.argv) < 3:
            print("Error: 'add' command requires a task title argument.")
            print_usage()
            return
        
        task_title = " ".join(sys.argv[2:])
        add_task(tasks, task_title)
        
    elif command == 'list':
        list_tasks(tasks)

    elif command == 'search':
        if len(sys.argv) < 3:
            print("Error: 'search' command requires a keyword argument.")
            print_usage()
            return
            
        keyword = " ".join(sys.argv[2:])
        search_tasks(tasks, keyword)
        
    else:
        print(f"Error: Unknown command '{command}'")
        print_usage()

if __name__ == "__main__":
    main()
