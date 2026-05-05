import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.trainings = []
        self.load_data()  # Загружаем данные из trainings.json при запуске
        self.create_widgets()

    def create_widgets(self):
        # Поля ввода (шаг 1)
        tk.Label(self.root, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Тип тренировки:").grid(row=1, column=0, padx=5, pady=5)
        self.type_entry = tk.Entry(self.root)
        self.type_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Длительность (мин):").grid(row=2, column=0, padx=5, pady=5)
        self.duration_entry = tk.Entry(self.root)
        self.duration_entry.grid(row=2, column=1, padx=5, pady=5)

        # Кнопка добавления (шаг 2)
        tk.Button(self.root, text="Добавить тренировку", command=self.add_training).grid(
            row=3, column=0, columnspan=2, pady=10
        )

        # Таблица для отображения данных
        self.tree = ttk.Treeview(self.root, columns=("Date", "Type", "Duration"), show="headings")
        self.tree.heading("Date", text="Дата")
        self.tree.heading("Type", text="Тип")
        self.tree.heading("Duration", text="Длительность (мин)")
        self.tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Фильтры (шаг 3)
        tk.Label(self.root, text="Фильтр по типу:").grid(row=5, column=0, padx=5, pady=5)
        self.filter_type = ttk.Combobox(self.root)
        self.filter_type.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Фильтр по дате:").grid(row=6, column=0, padx=5, pady=5)
        self.filter_date = tk.Entry(self.root)
        self.filter_date.grid(row=6, column=1, padx=5, pady=5)

        tk.Button(self.root, text="Применить фильтр", command=self.apply_filter).grid(row=7, column=0, pady=10)
        tk.Button(self.root, text="Сбросить фильтр", command=self.reset_filter).grid(row=7, column=1, pady=10)

    def add_training(self):
        date_str = self.date_entry.get()
        training_type = self.type_entry.get()
        duration_str = self.duration_entry.get()

        # Валидация даты (шаг 5)
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ГГГГ-ММ-ДД.")
            return

        # Валидация длительности (шаг 5)
        try:
            duration = int(duration_str)
            if duration <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Длительность должна быть положительным числом.")
            return

        # Добавляем в список и таблицу
        training = {"date": date_str, "type": training_type, "duration": duration}
        self.trainings.append(training)
        self.tree.insert("", "end", values=(date_str, training_type, duration))

        self.update_filter_options()
        self.save_data()  # Сохраняем в trainings.json (шаг 4)

        # Очищаем поля
        self.date_entry.delete(0, tk.END)
        self.type_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)

    def save_data(self):
        """Сохраняет данные в trainings.json (шаг 4)"""
        with open("trainings.json", "w", encoding="utf-8") as f:
            json.dump(self.trainings, f, ensure_ascii=False, indent=4)

    def load_data(self):
        """Загружает данные из trainings.json при запуске (шаг 4)"""
        if os.path.exists("trainings.json"):
            with open("trainings.json", "r", encoding="utf-8") as f:
                self.trainings = json.load(f)
            # Заполняем таблицу при загрузке
            for training in self.trainings:
                self.tree.insert("", "end", values=(training["date"], training["type"], training["duration"]))
            self.update_filter_options()

    def update_filter_options(self):
        types = list(set(t["type"] for t in self.trainings))
        self.filter_type["values"] = types

    def apply_filter(self):
        filter_type = self.filter_type.get()
        filter_date = self.filter_date.get()

        for item in self.tree.get_children():
            self.tree.delete(item)

        filtered = self.trainings
        if filter_type:
            filtered = [t for t in filtered if t["type"] == filter_type]
        if filter_date:
            filtered = [t for t in filtered if t["date"] == filter_date]

        for training in filtered:
            self.tree.insert("", "end", values=(training["date"], training["type"], training["duration"]))

    def reset_filter(self):
        self.filter_type.set("")
        self.filter_date.delete(0, tk.END)
        self.apply_filter()

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()
", command=self.reset_filter).grid(row=7, column=1, pady=10)
