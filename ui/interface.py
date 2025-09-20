import calendar
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.panel import Panel
from datetime import datetime
from core.task_manager import TaskManager
from core.weather_service import WeatherService
from core.calendar_manager import CalendarManager
from core.game_manager import TicTacToe, SimpleTetris
from core.password_generator import PasswordGenerator


class ShoriextUI:
    def __init__(self):
        self.console = Console()
        self.task_manager = TaskManager()
        self.weather_service = WeatherService()
        self.calendar_manager = CalendarManager()
        self.password_generator = PasswordGenerator()

    def show_ascii_art(self):
        ascii_art = r"""
███████╗██╗  ██╗ ██████╗ ██████╗ ██╗███████╗██╗  ██╗████████╗
██╔════╝██║  ██║██╔═══██╗██╔══██╗██║██╔════╝╚██╗██╔╝╚══██╔══╝
███████╗███████║██║   ██║██████╔╝██║█████╗   ╚███╔╝    ██║   
╚════██║██╔══██║██║   ██║██╔══██╗██║██╔══╝   ██╔██╗    ██║   
███████║██║  ██║╚██████╔╝██║  ██║██║███████╗██╔╝ ██╗   ██║   
╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝      
        """
        self.console.print(ascii_art, style="bold blue")
        self.console.print("=" * 70, style="bold blue")
        self.console.print(
            "🎯 shoriext - Универсальная консольная утилита", style="cyan"
        )
        self.console.print("=" * 70, style="bold blue")
        self.console.print("")

    def clear_screen(self):
        self.console.clear()

    def show_main_menu(self):
        self.show_ascii_art()
        self.console.print(
            Panel("[bold blue]🎯 Главное меню shoriext[/bold blue]", expand=False)
        )
        self.console.print("1. 📋 Трекер задач")
        self.console.print("2. 🌤️  Прогноз погоды (Москва)")
        self.console.print("3. 📅 Календарь")
        self.console.print("4. 🎮 Игры")
        self.console.print("5. 🔐 Генератор паролей")
        self.console.print("0. 🚪 Выйти")
        self.console.print("")

    # ==================== Task Tracker ====================
    def show_task_tracker_menu(self):
        while True:
            self.clear_screen()
            self.console.print(
                Panel("[bold green]📋 Трекер задач[/bold green]", expand=False)
            )
            self.console.print("1. 📋 Показать все задачи")
            self.console.print("2. ➕ Добавить новую задачу")
            self.console.print("3. ✅ Отметить прогресс")
            self.console.print("4. 📊 Статистика")
            self.console.print("5. 🔄 Сбросить задачу")
            self.console.print("6. 🗑️  Удалить задачу")
            self.console.print("0. 🔙 Назад")

            choice = Prompt.ask(
                "Выберите действие", choices=["0", "1", "2", "3", "4", "5", "6"]
            )

            if choice == "0":
                break
            elif choice == "1":
                self.show_tasks()
            elif choice == "2":
                self.add_task()
            elif choice == "3":
                self.increment_task()
            elif choice == "4":
                self.show_task_statistics()
            elif choice == "5":
                self.reset_task()
            elif choice == "6":
                self.remove_task()

            if choice != "0":
                Prompt.ask("\nНажмите Enter для продолжения...")

    def show_tasks(self):
        tasks = self.task_manager.get_all_tasks()
        if not tasks:
            self.console.print("[yellow]Нет созданных задач[/yellow]")
            return

        table = Table(
            title="📋 Ваши задачи", show_header=True, header_style="bold magenta"
        )
        table.add_column("Название", style="cyan")
        table.add_column("Описание", style="white")
        table.add_column("Приоритет", style="yellow")
        table.add_column("Прогресс", style="green")
        table.add_column("Статус", style="blue")

        for task in tasks:
            progress_text = f"{task.current_count}/{task.target_count}"
            priority_style = {"low": "green", "medium": "yellow", "high": "red"}.get(
                task.priority, "white"
            )
            priority_text = f"[{priority_style}]{task.priority}[/{priority_style}]"

            if task.completed_at:
                status = "[green]✅ Завершено[/green]"
            else:
                status = "[blue]⏳ В процессе[/blue]"

            table.add_row(
                task.name, task.description or "-", priority_text, progress_text, status
            )

        self.console.print(table)

    def add_task(self):
        self.console.print("\n[bold]➕ Добавление новой задачи[/bold]")
        name = Prompt.ask("Введите название задачи")
        if not name:
            self.console.print("[red]Название не может быть пустым![/red]")
            return

        if not self.task_manager.add_task(name):
            self.console.print("[red]Задача с таким названием уже существует![/red]")
            return

        description = Prompt.ask("Описание (необязательно)", default="")
        target_count = IntPrompt.ask("Целевое количество", default=1)
        priority = Prompt.ask(
            "Приоритет (low/medium/high)",
            choices=["low", "medium", "high"],
            default="medium",
        )

        # Обновляем задачу с новыми данными
        task = self.task_manager.get_task(name)
        task.description = description
        task.target_count = target_count
        task.priority = priority
        self.task_manager.save_data()

        self.console.print("[green]✅ Задача успешно добавлена![/green]")

    def increment_task(self):
        tasks = self.task_manager.get_all_tasks()
        if not tasks:
            self.console.print("[yellow]Нет задач для отметки прогресса[/yellow]")
            return

        self.console.print("\n[bold]Выберите задачу для отметки прогресса:[/bold]")
        for i, task in enumerate(tasks, 1):
            status = "✅" if task.completed_at else "⏳"
            self.console.print(f"{i}. {status} {task.name}")

        try:
            choice = IntPrompt.ask(
                "Введите номер задачи",
                choices=[str(i) for i in range(1, len(tasks) + 1)],
            )
            selected_task = tasks[choice - 1]

            if selected_task.increment():
                self.console.print("[green]✅ Прогресс отмечен![/green]")
                if selected_task.completed_at:
                    self.console.print(
                        f"[bold green]🎉 Поздравляем! Задача '{selected_task.name}' завершена![/bold green]"
                    )
            else:
                self.console.print("[yellow]Эта задача уже завершена![/yellow]")

        except (ValueError, IndexError):
            self.console.print("[red]Неверный выбор[/red]")

    def show_task_statistics(self):
        stats = self.task_manager.get_statistics()
        tasks = self.task_manager.get_all_tasks()

        table = Table(title="📊 Статистика задач", show_header=False)
        table.add_row("Всего задач", str(stats["total_tasks"]))
        table.add_row("Завершено", str(stats["completed_tasks"]))
        table.add_row("В процессе", str(stats["in_progress_tasks"]))
        table.add_row("Общий прогресс", stats["overall_progress"])

        self.console.print(table)

        if tasks:
            self.console.print("\n[bold]Детальный прогресс:[/bold]")
            for task in tasks:
                self.console.print(f"\n[cyan]{task.name}[/cyan]")
                progress_percentage = (
                    (task.current_count / task.target_count) * 100
                    if task.target_count > 0
                    else 0
                )
                progress_bar = "█" * int(progress_percentage // 5) + "░" * (
                    20 - int(progress_percentage // 5)
                )
                status = "✅ Завершено" if task.completed_at else "⏳ В процессе"
                self.console.print(f"  [{progress_bar}] {progress_percentage:.1f}%")
                self.console.print(
                    f"  {task.current_count}/{task.target_count} | {status}"
                )

    def reset_task(self):
        tasks = self.task_manager.get_all_tasks()
        if not tasks:
            self.console.print("[yellow]Нет задач для сброса[/yellow]")
            return

        self.console.print("\n[bold]Выберите задачу для сброса:[/bold]")
        for i, task in enumerate(tasks, 1):
            self.console.print(f"{i}. 🔄 {task.name}")

        try:
            choice = IntPrompt.ask(
                "Введите номер задачи",
                choices=[str(i) for i in range(1, len(tasks) + 1)],
            )
            selected_task = tasks[choice - 1]

            confirm = Prompt.ask(
                f"Вы уверены, что хотите сбросить '{selected_task.name}'? (y/N)",
                default="n",
            )
            if confirm.lower() == "y":
                self.task_manager.reset_task(selected_task.name)
                self.console.print("[green]✅ Задача сброшена![/green]")
            else:
                self.console.print("[yellow]Сброс отменен[/yellow]")

        except (ValueError, IndexError):
            self.console.print("[red]Неверный выбор[/red]")

    def remove_task(self):
        tasks = self.task_manager.get_all_tasks()
        if not tasks:
            self.console.print("[yellow]Нет задач для удаления[/yellow]")
            return

        self.console.print("\n[bold]Выберите задачу для удаления:[/bold]")
        for i, task in enumerate(tasks, 1):
            status = "✅" if task.completed_at else "⏳"
            self.console.print(f"{i}. {status} {task.name}")

        try:
            choice = IntPrompt.ask(
                "Введите номер задачи",
                choices=[str(i) for i in range(1, len(tasks) + 1)],
            )
            selected_task = tasks[choice - 1]

            confirm = Prompt.ask(
                f"Вы уверены, что хотите удалить '{selected_task.name}'? (y/N)",
                default="n",
            )
            if confirm.lower() == "y":
                self.task_manager.remove_task(selected_task.name)
                self.console.print("[green]✅ Задача удалена![/green]")
            else:
                self.console.print("[yellow]Удаление отменено[/yellow]")

        except (ValueError, IndexError):
            self.console.print("[red]Неверный выбор[/red]")

    # ==================== Weather ====================
    def show_weather(self):
        self.clear_screen()
        self.console.print(
            Panel("[bold yellow]🌤️ Прогноз погоды в Москве[/bold yellow]", expand=False)
        )

        try:
            forecast = self.weather_service.get_moscow_weather_forecast()

            table = Table(
                title="Прогноз на неделю", show_header=True, header_style="bold blue"
            )
            table.add_column("Дата", style="cyan")
            table.add_column("День недели", style="white")
            table.add_column("Погода", style="yellow")
            table.add_column("Температура", style="green")
            table.add_column("Сегодня", style="red")

            for day in forecast:
                today_mark = "✓" if day["is_today"] else ""
                temp_range = f"{day['temp_min']}°C / {day['temp_max']}°C"

                table.add_row(
                    day["date"],
                    day["day_of_week"],
                    day["condition"],
                    temp_range,
                    today_mark,
                )

            self.console.print(table)

        except Exception as e:
            self.console.print(f"[red]Ошибка получения погоды: {e}[/red]")

        Prompt.ask("\nНажмите Enter для продолжения...")

    # ==================== Calendar ====================
    def show_calendar_menu(self):
        while True:
            self.clear_screen()
            self.console.print(
                Panel("[bold magenta]📅 Календарь[/bold magenta]", expand=False)
            )
            self.console.print("1. 📅 Просмотр календаря")
            self.console.print("2. 📋 Показать все события")
            self.console.print("3. ➕ Добавить событие")
            self.console.print("4. 🗑️  Удалить событие")
            self.console.print("5. 🔮 Ближайшие события")
            self.console.print("0. 🔙 Назад")

            choice = Prompt.ask(
                "Выберите действие", choices=["0", "1", "2", "3", "4", "5"]
            )

            if choice == "0":
                break
            elif choice == "1":
                self.show_calendar_view()
            elif choice == "2":
                self.show_calendar_events()
            elif choice == "3":
                self.add_calendar_event()
            elif choice == "4":
                self.remove_calendar_event()
            elif choice == "5":
                self.show_upcoming_events()

            if choice != "0":
                Prompt.ask("\nНажмите Enter для продолжения...")

    def show_calendar_events(self):
        events = self.calendar_manager.events
        if not events:
            self.console.print("[yellow]Нет запланированных событий[/yellow]")
            return

        table = Table(
            title="📅 Все события", show_header=True, header_style="bold magenta"
        )
        table.add_column("Дата", style="cyan")
        table.add_column("Название", style="white")
        table.add_column("Описание", style="green")
        table.add_column("Тип", style="yellow")

        # Сортируем события по дате
        sorted_events = sorted(events, key=lambda x: x.date)

        for event in sorted_events:
            event_type_style = {
                "personal": "blue",
                "work": "red",
                "holiday": "green",
            }.get(event.event_type, "white")
            type_text = f"[{event_type_style}]{event.event_type}[/{event_type_style}]"

            table.add_row(event.date, event.title, event.description or "-", type_text)

        self.console.print(table)

    def add_calendar_event(self):
        self.console.print("\n[bold]➕ Добавление нового события[/bold]")
        title = Prompt.ask("Название события")
        if not title:
            self.console.print("[red]Название не может быть пустым![/red]")
            return

        date = Prompt.ask("Дата (ГГГГ-ММ-ДД)")
        description = Prompt.ask("Описание (необязательно)", default="")
        event_type = Prompt.ask(
            "Тип события", choices=["personal", "work", "holiday"], default="personal"
        )

        try:
            self.calendar_manager.add_event(title, date, description, event_type)
            self.console.print("[green]✅ Событие успешно добавлено![/green]")
        except Exception as e:
            self.console.print(f"[red]Ошибка добавления события: {e}[/red]")

    def remove_calendar_event(self):
        events = self.calendar_manager.events
        if not events:
            self.console.print("[yellow]Нет событий для удаления[/yellow]")
            return

        self.console.print("\n[bold]Выберите событие для удаления:[/bold]")
        for i, event in enumerate(events, 1):
            self.console.print(f"{i}. {event.date} - {event.title}")

        try:
            choice = IntPrompt.ask(
                "Введите номер события",
                choices=[str(i) for i in range(1, len(events) + 1)],
            )
            selected_event = events[choice - 1]

            confirm = Prompt.ask(
                f"Вы уверены, что хотите удалить '{selected_event.title}'? (y/N)",
                default="n",
            )
            if confirm.lower() == "y":
                self.calendar_manager.remove_event(
                    selected_event.title, selected_event.date
                )
                self.console.print("[green]✅ Событие удалено![/green]")
            else:
                self.console.print("[yellow]Удаление отменено[/yellow]")

        except (ValueError, IndexError):
            self.console.print("[red]Неверный выбор[/red]")

    def show_upcoming_events(self):
        upcoming = self.calendar_manager.get_upcoming_events(7)
        if not upcoming:
            self.console.print("[yellow]Нет событий на ближайшие 7 дней[/yellow]")
            return

        self.console.print("\n[bold]🔮 События на ближайшие 7 дней:[/bold]")
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("Дата", style="cyan")
        table.add_column("Название", style="white")
        table.add_column("Описание", style="green")

        for event in upcoming:
            table.add_row(event.date, event.title, event.description or "-")

        self.console.print(table)

    def show_calendar_view(self):
        """Показать визуальный календарь"""
        today = datetime.now()
        year = today.year
        month = today.month

        while True:
            self.clear_screen()
            self.console.print(
                Panel(
                    f"[bold blue]📅 Календарь - {self.get_month_name(month)} {year}[/bold blue]",
                    expand=False,
                )
            )

            # Показываем календарь
            self.display_month_calendar(year, month)

            self.console.print("\n[bold]Навигация:[/bold]")
            self.console.print("← → : Переключение месяцев")
            self.console.print("Enter: Выбрать день")
            self.console.print("0: Назад")

            nav_choice = Prompt.ask(
                "Выберите действие", choices=["0", "1", "2", "enter"]
            )

            if nav_choice == "0":
                break
            elif nav_choice == "1":
                # Предыдущий месяц
                if month == 1:
                    month = 12
                    year -= 1
                else:
                    month -= 1
            elif nav_choice == "2":
                # Следующий месяц
                if month == 12:
                    month = 1
                    year += 1
                else:
                    month += 1
            elif nav_choice == "enter":
                self.select_day_events(year, month)

    def display_month_calendar(self, year: int, month: int):
        """Отобразить календарь месяца"""
        # Получаем события для текущего месяца
        events_dict = self.calendar_manager.get_events_for_calendar(year, month)

        # Создаем календарь
        cal = calendar.monthcalendar(year, month)

        # Заголовки дней недели
        days_header = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        self.console.print(" ".join(f"[bold]{day:2}[/bold]" for day in days_header))

        today = datetime.now()

        # Отображаем недели
        for week in cal:
            week_str = ""
            for i, day in enumerate(week):
                if day == 0:
                    week_str += "   "
                else:
                    date_str = f"{year}-{month:02d}-{day:02d}"
                    has_events = date_str in events_dict

                    # Проверяем, является ли сегодняшним днем
                    is_today = (
                        year == today.year and month == today.month and day == today.day
                    )

                    if is_today:
                        day_str = f"[bold red]{day:2}[/bold red]"
                    elif has_events:
                        day_str = f"[bold yellow]{day:2}[/bold yellow]"
                    else:
                        day_str = f"{day:2}"

                    week_str += day_str + " "

            self.console.print(week_str)

        # Легенда
        self.console.print("\n[bold]Легенда:[/bold]")
        self.console.print("[red]●[/red] Сегодня")
        self.console.print("[yellow]●[/yellow] Есть события")

    def get_month_name(self, month: int) -> str:
        """Получить название месяца на русском"""
        months = {
            1: "Январь",
            2: "Февраль",
            3: "Март",
            4: "Апрель",
            5: "Май",
            6: "Июнь",
            7: "Июль",
            8: "Август",
            9: "Сентябрь",
            10: "Октябрь",
            11: "Ноябрь",
            12: "Декабрь",
        }
        return months.get(month, "")

    def select_day_events(self, year: int, month: int):
        """Выбрать день и показать события"""
        try:
            day = IntPrompt.ask("Введите день")
            if day < 1 or day > 31:
                self.console.print("[red]Неверный день![/red]")
                return

            date_str = f"{year}-{month:02d}-{day:02d}"
            events = self.calendar_manager.get_events_by_date(date_str)

            self.clear_screen()
            self.console.print(
                Panel(f"[bold blue]📅 События на {date_str}[/bold blue]", expand=False)
            )

            if not events:
                self.console.print("[yellow]Нет событий на этот день[/yellow]")
            else:
                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("Название", style="cyan")
                table.add_column("Описание", style="white")
                table.add_column("Тип", style="yellow")

                for event in events:
                    event_type_style = {
                        "personal": "blue",
                        "work": "red",
                        "holiday": "green",
                    }.get(event.event_type, "white")
                    type_text = (
                        f"[{event_type_style}]{event.event_type}[/{event_type_style}]"
                    )

                    table.add_row(event.title, event.description or "-", type_text)

                self.console.print(table)

            # Возможность добавить событие на этот день
            add_event = Prompt.ask("Добавить событие на этот день? (y/N)", default="n")
            if add_event.lower() == "y":
                title = Prompt.ask("Название события")
                description = Prompt.ask("Описание (необязательно)", default="")
                event_type = Prompt.ask(
                    "Тип события",
                    choices=["personal", "work", "holiday"],
                    default="personal",
                )

                self.calendar_manager.add_event(
                    title, date_str, description, event_type
                )
                self.console.print("[green]✅ Событие добавлено![/green]")

        except Exception as e:
            self.console.print(f"[red]Ошибка: {e}[/red]")

    # ==================== Games ====================
    def show_games_menu(self):
        while True:
            self.clear_screen()
            self.console.print(Panel("[bold red]🎮 Игры[/bold red]", expand=False))
            self.console.print("1. ❌⭕ Крестики-нолики")
            self.console.print("2. 🧱 Тетрис (упрощенный)")
            self.console.print("0. 🔙 Назад")

            choice = Prompt.ask("Выберите игру", choices=["0", "1", "2"])

            if choice == "0":
                break
            elif choice == "1":
                self.play_tic_tac_toe()
            elif choice == "2":
                self.play_tetris_demo()

            if choice != "0":
                Prompt.ask("\nНажмите Enter для продолжения...")

    def play_tic_tac_toe(self):
        self.clear_screen()
        self.console.print(
            Panel("[bold green]❌⭕ Крестики-нолики[/bold green]", expand=False)
        )

        game = TicTacToe()

        while True:
            self.console.print(game.display_board())

            winner = game.check_winner()
            if winner:
                if winner == "Draw":
                    self.console.print("[yellow]Ничья![/yellow]")
                else:
                    self.console.print(f"[bold green]Победитель: {winner}[/bold green]")
                break

            try:
                position = IntPrompt.ask(
                    f"Игрок {game.current_player}, введите позицию (0-8)"
                )
                if game.make_move(position):
                    game.switch_player()
                else:
                    self.console.print("[red]Неверный ход! Попробуйте снова.[/red]")
            except ValueError:
                self.console.print("[red]Введите число от 0 до 8[/red]")

        play_again = Prompt.ask("Сыграть еще раз? (y/N)", default="n")
        if play_again.lower() == "y":
            self.play_tic_tac_toe()

    def play_tetris_demo(self):
        self.clear_screen()
        self.console.print(
            Panel("[bold cyan]🧱 Тетрис (демонстрация)[/bold cyan]", expand=False)
        )

        tetris = SimpleTetris()
        tetris.current_piece = tetris.create_random_piece()

        self.console.print(tetris.display_board())
        self.console.print(
            "[yellow]Это упрощенная версия Тетриса для демонстрации[/yellow]"
        )
        self.console.print("В полной версии будут реализованы:")
        self.console.print("• Падение фигур")
        self.console.print("• Вращение фигур")
        self.console.print("• Удаление заполненных линий")
        self.console.print("• Система очков")

    # ==================== Password Generator ====================
    def show_password_generator(self):
        while True:
            self.clear_screen()
            self.console.print(
                Panel("[bold purple]🔐 Генератор паролей[/bold purple]", expand=False)
            )
            self.console.print("1. 🎲 Сгенерировать пароли")
            self.console.print("2. 🔍 Проверить надежность пароля")
            self.console.print("0. 🔙 Назад")

            choice = Prompt.ask("Выберите действие", choices=["0", "1", "2"])

            if choice == "0":
                break
            elif choice == "1":
                self.generate_passwords()
            elif choice == "2":
                self.check_password_strength()

            if choice != "0":
                Prompt.ask("\nНажмите Enter для продолжения...")

    def generate_passwords(self):
        self.console.print("\n[bold]🎲 Генерация паролей[/bold]")

        try:
            count = IntPrompt.ask("Количество паролей", default=5)
            length = IntPrompt.ask("Длина пароля", default=12)

            use_uppercase = (
                Prompt.ask("Использовать заглавные буквы? (Y/n)", default="y").lower()
                == "y"
            )
            use_lowercase = (
                Prompt.ask("Использовать строчные буквы? (Y/n)", default="y").lower()
                == "y"
            )
            use_digits = (
                Prompt.ask("Использовать цифры? (Y/n)", default="y").lower() == "y"
            )
            use_special = (
                Prompt.ask(
                    "Использовать специальные символы? (Y/n)", default="y"
                ).lower()
                == "y"
            )

            passwords = self.password_generator.generate_multiple_passwords(
                count=count,
                length=length,
                use_uppercase=use_uppercase,
                use_lowercase=use_lowercase,
                use_digits=use_digits,
                use_special=use_special,
            )

            self.console.print("\n[bold]Сгенерированные пароли:[/bold]")
            for i, password in enumerate(passwords, 1):
                self.console.print(f"{i}. {password}")

        except Exception as e:
            self.console.print(f"[red]Ошибка генерации паролей: {e}[/red]")

    def check_password_strength(self):
        self.console.print("\n[bold]🔍 Проверка надежности пароля[/bold]")
        password = Prompt.ask("Введите пароль для проверки")

        if not password:
            self.console.print("[yellow]Пароль не может быть пустым[/yellow]")
            return

        result = self.password_generator.check_password_strength(password)

        self.console.print(f"\n[bold]Результаты проверки:[/bold]")
        self.console.print(
            f"Надежность: [bold]{result['strength']}[/bold] ({result['score']}/5)"
        )

        if result["feedback"]:
            self.console.print("\n[bold]Рекомендации:[/bold]")
            for feedback in result["feedback"]:
                self.console.print(f"• {feedback}")
        else:
            self.console.print("[green]✅ Пароль надежный![/green]")

    # ==================== Main Loop ====================
    def run(self):
        while True:
            self.clear_screen()
            self.show_main_menu()

            try:
                choice = Prompt.ask(
                    "Выберите раздел", choices=["0", "1", "2", "3", "4", "5"]
                )

                if choice == "0":
                    self.console.print(
                        "[blue]👋 До свидания! Спасибо за использование shoriext![/blue]"
                    )
                    break
                elif choice == "1":
                    self.show_task_tracker_menu()
                elif choice == "2":
                    self.show_weather()
                elif choice == "3":
                    self.show_calendar_menu()
                elif choice == "4":
                    self.show_games_menu()
                elif choice == "5":
                    self.show_password_generator()

            except KeyboardInterrupt:
                self.console.print("\n\n[blue]👋 До свидания![/blue]")
                break
            except Exception as e:
                self.console.print(f"[red]Ошибка: {e}[/red]")
                Prompt.ask("Нажмите Enter для продолжения...")


if __name__ == "__main__":
    ui = ShoriextUI()
    ui.run()
