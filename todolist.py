import csv
import os
from datetime import datetime

FILE_NAME = "tasks.csv"


def todoModule():
    appState = {"nextId": 1, "tasks": loadTasks()}
    if appState["tasks"]:
        appState["nextId"] = max(int(t["id"]) for t in appState["tasks"]) + 1
    print("To-Do List Manager")
    print("-")
    return mainMenu(appState)


def loadTasks():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


def saveTasks(tasks):
    with open(FILE_NAME, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(
            f, fieldnames=["id", "title", "description", "added_on", "due_date", "status"]
        )
        writer.writeheader()
        writer.writerows(tasks)


def mainMenu(appState):
    while True:
        print("Main Menu:")
        print("1) View All Tasks")
        print("2) Add New Task")
        print("3) Mark Task as Done")
        print("4) Edit Task")
        print("5) Delete Task")
        print("6) Exit")
        choice = input("Choose (1-6): ").strip()
        if choice == "1":
            viewTasks(appState)
        elif choice == "2":
            addTask(appState)
        elif choice == "3":
            markTaskDone(appState)
        elif choice == "4":
            editTask(appState)
        elif choice == "5":
            deleteTask(appState)
        elif choice == "6":
            print("Goodbye!")
            return None
        else:
            print("Please choose a valid option.")


def promptNonEmpty(promptText):
    value = input(promptText).strip()
    if value == "":
        print("Please enter a value.")
        return promptNonEmpty(promptText)
    return value


def promptDate(promptText):
    value = input(promptText + " (YYYY-MM-DD or leave blank): ").strip()
    if value == "":
        return ""
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return value
    except ValueError:
        print("Invalid date format.")
        return promptDate(promptText)


def viewTasks(appState):
    tasks = appState["tasks"]
    if not tasks:
        print("No tasks found.")
        print("-")
        return
    print("-")
    print("Current Tasks:")
    for t in tasks:
        print(f"{t['id']}) {t['title']} [{t['status']}]")
        print(f"   Added: {t['added_on']} | Due: {t['due_date'] or 'N/A'}")
        if t["description"]:
            print(f"   Description: {t['description']}")
    print("-")


def addTask(appState):
    title = promptNonEmpty("Task title: ")
    description = input("Description (optional): ").strip()
    due_date = promptDate("Due date")
    added_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    newTask = {
        "id": str(appState["nextId"]),
        "title": title,
        "description": description,
        "added_on": added_on,
        "due_date": due_date,
        "status": "pending"
    }
    appState["tasks"].append(newTask)
    appState["nextId"] += 1
    saveTasks(appState["tasks"])
    print("Task added.")
    print("-")


def selectTask(appState):
    tasks = appState["tasks"]
    if not tasks:
        print("No tasks found.")
        return None
    for t in tasks:
        print(f"{t['id']}) {t['title']} [{t['status']}]")
    txt = input("Choose task ID: ").strip()
    if txt.isdigit() and any(t["id"] == txt for t in tasks):
        return txt
    print("Invalid ID.")
    return selectTask(appState)


def markTaskDone(appState):
    taskId = selectTask(appState)
    if taskId is None:
        return
    for t in appState["tasks"]:
        if t["id"] == taskId:
            t["status"] = "done"
            saveTasks(appState["tasks"])
            print("Task marked as done.")
            print("-")
            return


def editTask(appState):
    taskId = selectTask(appState)
    if taskId is None:
        return
    for t in appState["tasks"]:
        if t["id"] == taskId:
            print("Edit Menu:")
            print("1) Edit Title")
            print("2) Edit Description")
            print("3) Edit Due Date")
            print("4) Back")
            choice = input("Choose (1-4): ").strip()
            if choice == "1":
                t["title"] = promptNonEmpty("New title: ")
            elif choice == "2":
                t["description"] = input("New description: ").strip()
            elif choice == "3":
                t["due_date"] = promptDate("New due date")
            elif choice == "4":
                return
            else:
                print("Invalid option.")
                return editTask(appState)
            saveTasks(appState["tasks"])
            print("Task updated.")
            print("-")
            return


def deleteTask(appState):
    taskId = selectTask(appState)
    if taskId is None:
        return
    updated = [t for t in appState["tasks"] if t["id"] != taskId]
    if len(updated) != len(appState["tasks"]):
        appState["tasks"] = updated
        saveTasks(appState["tasks"])
        print("Task deleted.")
        print("-")
    else:
        print("Invalid task ID.")


if __name__ == "__main__":
    todoModule()
