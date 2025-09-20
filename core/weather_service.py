import requests
from datetime import datetime, timedelta


class WeatherService:
    def __init__(self):
        # В реальной реализации здесь был бы API ключ
        # self.api_key = "your_api_key"
        pass

    def get_moscow_weather_forecast(self):
        """Имитация получения погоды для Москвы на неделю"""
        # Это имитация данных - в реальном приложении здесь был бы API вызов
        days = []
        today = datetime.now()

        # Имитационные данные
        weather_conditions = ["Солнечно", "Облачно", "Дождь", "Снег", "Гроза"]
        temperatures = [(-5, 2), (0, 5), (5, 12), (10, 18), (15, 25), (20, 30)]

        for i in range(7):
            date = today + timedelta(days=i)
            temp_range = temperatures[i % len(temperatures)]

            day_data = {
                "date": date.strftime("%d.%m.%Y"),
                "day_of_week": self.get_day_of_week(date.weekday()),
                "condition": weather_conditions[i % len(weather_conditions)],
                "temp_min": temp_range[0],
                "temp_max": temp_range[1],
                "is_today": i == 0,
            }
            days.append(day_data)

        return days

    def get_day_of_week(self, weekday):
        days = [
            "Понедельник",
            "Вторник",
            "Среда",
            "Четверг",
            "Пятница",
            "Суббота",
            "Воскресенье",
        ]
        return days[weekday]
