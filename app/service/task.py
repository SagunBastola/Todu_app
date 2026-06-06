from pathlib import Path
import json
from typing import Dict,List
data_file=Path(__file__).parent.parent/"data"/"work.json"

def get_tasks(id : int):
    tasks=get_all_tasks()

    for task in tasks:
        if task["id"] == id :
            return {"task" : task}
    raise ValueError("No Task of the mentioned id was found!!")

def get_all_tasks():
    try:
        with open(data_file,"r",encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def search_similar_tasks(name : str):
    needle=name.strip().lower()
    tasks=get_all_tasks()
    if needle:
        task=[t for t in tasks if needle in t.get("name","")]
    if not task:
        raise ValueError("No Matching Task")
    total=len(task)
    return {"total":total , "items" : task}

def priority_listing(priority : str):
    tasks=get_all_tasks()
    priority=priority.strip().capitalize()
    task=[t for t in tasks if priority in t.get("priority","")]
    if not task:
        return {"total" : 0 ,"task" : f"No task of {priority} priority"}
    total=len(task)
    return {"total": total , "task" : task}

def add_task(task : Dict) -> Dict:
    tasks=get_all_tasks()
    if any(task["id"] == t.get("id") for t in tasks):
        raise ValueError("Not Valid id for the task")
    tasks.append(task)
    save_task(tasks)
    return task

def save_task(tasks : List[Dict]):
    with open(data_file,mode="w",encoding="utf-8") as file:
        json.dump(tasks,file,indent=2,ensure_ascii=False)
        


def delete_task(task_id : int):
    tasks=get_all_tasks()
    for idx,t in enumerate(tasks):
        if t["id"] == task_id:
            deleted=tasks.pop(idx)
            save_task(tasks)
            return {"data":deleted}
    return {"result":"Task id doesn't exist"}

def change_task(task_id : int , update_data : Dict):
    tasks=get_all_tasks()

    for idx,t in enumerate(tasks):
        if t["id"] == task_id:
            t.update(update_data)
            tasks[idx] = t
            save_task(tasks)
            return t
    raise ValueError("error ")