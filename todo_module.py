from datetime import datetime

def get_tasks(ds, reg):
    """Return list of tasks for reg (live list from datastore)."""
    return ds.todo_for(reg)

def add_task(ds, reg, text):
    if not text:
        return False
    tasks = ds.todo_for(reg)
    tasks.append({"text": text, "state": "Pending", "date": datetime.today().strftime("%Y-%m-%d")})
    ds.save()
    return True

def mark_done(ds, reg, index):
    tasks = ds.todo_for(reg)
    if 0 <= index < len(tasks):
        tasks[index]["state"] = "Done"
        ds.save()
        return True
    return False

def delete_task(ds, reg, index):
    tasks = ds.todo_for(reg)
    if 0 <= index < len(tasks):
        tasks.pop(index)
        ds.save()
        return True
    return False
