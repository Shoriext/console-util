import json
import os
from datetime import datetime
from typing import Dict, List


class Task:
    def __init__(
        self,
        name: str,
        description: str = "",
        target_count: int = 1,
        priority: str = "medium",
    ):
        self.name = name
        self.description = description
        self.target_count = target_count
        self.current_count = 0
        self.priority = priority  # low, medium, high
        self.created_at = datetime.now().isoformat()
        self.completed_at = None
        self.history = []

    def increment(self):
        if self.current_count < self.target_count:
            self.current_count += 1
            self.history.append(
                {"timestamp": datetime.now().isoformat(), "action": "increment"}
            )
            if self.current_count >= self.target_count:
                self.completed_at = datetime.now().isoformat()
            return True
        return False

    def reset(self):
        self.current_count = 0
        self.completed_at = None
        self.history.append(
            {"timestamp": datetime.now().isoformat(), "action": "reset"}
        )

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "target_count": self.target_count,
            "current_count": self.current_count,
            "priority": self.priority,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
            "history": self.history,
        }

    @classmethod
    def from_dict(cls, data):
        task = cls(
            data["name"],
            data.get("description", ""),
            data.get("target_count", 1),
            data.get("priority", "medium"),
        )
        task.current_count = data.get("current_count", 0)
        task.created_at = data.get("created_at", datetime.now().isoformat())
        task.completed_at = data.get("completed_at")
        task.history = data.get("history", [])
        return task


class TaskManager:
    def __init__(self, data_file: str = "data/tasks.json"):
        self.data_file = data_file
        self.tasks: Dict[str, Task] = {}
        self.load_data()

    def load_data(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for task_name, task_data in data.items():
                        self.tasks[task_name] = Task.from_dict(task_data)
            except Exception as e:
                print(f"Ошибка загрузки данных: {e}")

    def save_data(self):
        try:
            data = {name: task.to_dict() for name, task in self.tasks.items()}
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения данных: {e}")

    def add_task(
        self,
        name: str,
        description: str = "",
        target_count: int = 1,
        priority: str = "medium",
    ):
        if name in self.tasks:
            return False
        self.tasks[name] = Task(name, description, target_count, priority)
        self.save_data()
        return True

    def increment_task(self, name: str):
        if name in self.tasks:
            result = self.tasks[name].increment()
            self.save_data()
            return result
        return False

    def reset_task(self, name: str):
        if name in self.tasks:
            self.tasks[name].reset()
            self.save_data()
            return True
        return False

    def remove_task(self, name: str):
        if name in self.tasks:
            del self.tasks[name]
            self.save_data()
            return True
        return False

    def get_task(self, name: str):
        return self.tasks.get(name)

    def get_all_tasks(self):
        return list(self.tasks.values())

    def get_statistics(self):
        total_tasks = len(self.tasks)
        completed_tasks = sum(1 for task in self.tasks.values() if task.completed_at)
        total_progress = sum(task.current_count for task in self.tasks.values())
        total_target = sum(task.target_count for task in self.tasks.values())

        if total_target > 0:
            overall_percentage = (total_progress / total_target) * 100
        else:
            overall_percentage = 0

        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "in_progress_tasks": total_tasks - completed_tasks,
            "overall_progress": f"{overall_percentage:.1f}%",
        }
