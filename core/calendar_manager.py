import json
import os
from datetime import datetime, timedelta
from typing import Dict, List


class CalendarEvent:
    def __init__(
        self, title: str, date: str, description: str = "", event_type: str = "personal"
    ):
        self.title = title
        self.date = date  # формат: YYYY-MM-DD
        self.description = description
        self.event_type = event_type  # personal, work, holiday
        self.created_at = datetime.now().isoformat()

    def to_dict(self):
        return {
            "title": self.title,
            "date": self.date,
            "description": self.description,
            "event_type": self.event_type,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data):
        event = cls(
            data["title"],
            data["date"],
            data.get("description", ""),
            data.get("event_type", "personal"),
        )
        event.created_at = data.get("created_at", datetime.now().isoformat())
        return event


class CalendarManager:
    def __init__(self, data_file: str = "data/calendar.json"):
        self.data_file = data_file
        self.events: List[CalendarEvent] = []
        self.load_data()

    def load_data(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.events = [
                        CalendarEvent.from_dict(event_data) for event_data in data
                    ]
            except Exception as e:
                print(f"Ошибка загрузки данных календаря: {e}")

    def save_data(self):
        try:
            data = [event.to_dict() for event in self.events]
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения данных календаря: {e}")

    def add_event(
        self, title: str, date: str, description: str = "", event_type: str = "personal"
    ):
        event = CalendarEvent(title, date, description, event_type)
        self.events.append(event)
        self.save_data()
        return True

    def get_events_by_date(self, date: str) -> List[CalendarEvent]:
        return [event for event in self.events if event.date == date]

    def get_events_by_month(self, year: int, month: int) -> List[CalendarEvent]:
        events = []
        for event in self.events:
            event_date = datetime.strptime(event.date, "%Y-%m-%d")
            if event_date.year == year and event_date.month == month:
                events.append(event)
        return events

    def get_upcoming_events(self, days: int = 7) -> List[CalendarEvent]:
        """Получить события на ближайшие N дней"""
        upcoming = []
        today = datetime.now()
        for event in self.events:
            event_date = datetime.strptime(event.date, "%Y-%m-%d")
            if 0 <= (event_date - today).days <= days:
                upcoming.append(event)
        return sorted(upcoming, key=lambda x: x.date)

    def remove_event(self, title: str, date: str) -> bool:
        initial_count = len(self.events)
        self.events = [
            event
            for event in self.events
            if not (event.title == title and event.date == date)
        ]
        if len(self.events) < initial_count:
            self.save_data()
            return True
        return False

    def get_events_for_calendar(
        self, year: int, month: int
    ) -> Dict[str, List[CalendarEvent]]:
        """Возвращает словарь {дата: [события]} для календаря"""
        events_dict = {}
        events = self.get_events_by_month(year, month)
        for event in events:
            if event.date not in events_dict:
                events_dict[event.date] = []
            events_dict[event.date].append(event)
        return events_dict
