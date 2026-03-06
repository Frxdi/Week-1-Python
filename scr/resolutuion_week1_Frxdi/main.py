import argparse
import sys
import os
import json
#Vars
TASKS_FILE = "tasks.json"

#Importing Json
def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return[]
    with open(TASKS_FILE, "r") as file:
        return json.load(file)

#Saving Tasks
def save_task(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=2)
        
def main():
    #Create Parsers
    parser = argparse.ArgumentParser()
    parser.add_argument("task", type=str, nargs="?", help="Task to add")
    parser.add_argument("-l", "--list", help="List all tasks", action="store_true")
    parser.add_argument("-c", "--complete", type=int, help="Mark a task as complete by ID")
    parser.add_argument("-d", "--delete", type=int, help="Delete a task by ID")
    parser.add_argument("-dt", "--deletetask", type=str, help="Delete a task by Name")
    parser.add_argument("-ct", "--completetask", type=str, help="Mark a task as complete by Name")
    args = parser.parse_args()

    #Default Help
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    #List Tasks
    if args.list:
        tasks = load_tasks()
        for task in tasks:
            status = "x" if task["done"] else " "
            print(f"[{status}] {task['id']}: {task['task']}")
        sys.exit(0)

    #Complete Tasks by ID
    elif args.complete:
        tasks = load_tasks()
        for task in tasks:
            if task["id"] == args.complete:
                task["done"] = True
                save_task(tasks)
                print(f"Task {args.complete} marked as complete")
                break
            else:
                print("Task ID not found")
                break

    #Complete Tasks by Name
    elif args.completetask:
        tasks = load_tasks()
        for task in tasks:
            if task["task"] == args.completetask:
                task["done"] = True
                save_task(tasks)
                print(f"Task {args.completetask} marked as complete")
                break      
            else:
                print("Task Name not found")
                break

    #Delete Tasks by ID
    elif args.delete:
        tasks = load_tasks()
        new_tasks = []
        for task in tasks:
            if task["id"] != args.delete:
                new_tasks.append(task)
        task = new_tasks
        save_task(new_tasks)
        print(f"Task {args.delete} deleted")

    #Delete Tasks by Name 
    elif args.deletetask:
        tasks = load_tasks()
        new_tasks = []
        for task in tasks:
            if task["task"] != args.deletetask:
                new_tasks.append(task)
        task = new_tasks
        save_task(new_tasks)
        print(f"Task {args.deletetask} deleted")
    
    #Create new Tasks 
    elif args.task:
        tasks = load_tasks()
        if len(tasks) == 0:
            new_id = 1
        else:
            new_id = tasks[-1]["id"] + 1
        tasks.append({"id": new_id, "task": args.task, "done": False})
        save_task(tasks)

        print(f"Task {args.task} added with ID of {new_id}")

if __name__ == "__main__":
    main()

