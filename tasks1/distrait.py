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
        # Explicitly setting encoding to UTF-8 for better compatibility, 
        # though the main fix is removing problematic characters.
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            if not content:
                return []
            return json.loads(content)
    except (json.JSONDecodeError, Exception) as e:
        # A safer failure mode is to discard corrupted data and start fresh
        print(f"Warning: Distrait data file is corrupted or unreadable ({e}). Starting with a clean slate.")
        return []

def save_tasks(tasks: List[Dict[str, Any]]):
    """Saves the current list of tasks to the JSON file."""
    try:
        # Ensure we write using UTF-8 encoding
        with open(TASKS_FILE, 'w', encoding='utf-8') as f:
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
    # Replaced emoji (✅) with ASCII [OK]
    print(f"\n[OK] Task '{task_title}' (ID: {task_id}) added successfully to Distrait.")

# Removed complete_task function

def display_tasks(tasks: List[Dict[str, Any]], title: str):
    """Helper function to display a list of tasks."""
    if not tasks:
        print(f"\nNo tasks found in the {title.lower()} list.")
        return

    print(f"\n--- Distrait: {title} ---")
    
    for task in tasks:
        # Replaced emojis (✅, ⏳) and ANSI color codes with pure ASCII symbols/formatting
        if task['status'] == 'complete':
            status_symbol = "[X]" # Done
        else:
            status_symbol = "[ ]" # Pending
        
        # Removed color codes to ensure maximum compatibility across terminals
        
        print(
            f"{status_symbol} ({task['id']}) {task['title']}"
        )
    print("-" * (len(title) + 19))

def list_tasks(tasks: List[Dict[str, Any]]):
    """Displays all tasks."""
    list_tasks_to_display = sorted(tasks, key=lambda t: t['id'])
    display_tasks(list_tasks_to_display, "ALL Tasks")

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
        
    # Removed elif command == 'complete' block
        
    else:
        print(f"Error: Unknown command '{command}'")
        print_usage()

if __name__ == "__main__":
    main()
