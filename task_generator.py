import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Планировщик тренировок")
        self.root.geometry("900x600")
        self.root.configure(bg='#f0f0f0')
        
        # Хранилище тренировок
        self.trainings = []
        self.json_file = "trainings.json"
        
        self.load_data()
        self.setup_ui()
    
    def setup_ui(self):
        # Заголовок
        title = tk.Label(self.root, text="🏋️ Планировщик тренировок", 
                        font=("Arial", 18, "bold"), bg='#f0f0f0')
        title.pack(pady=10)
        
        # Рамка для добавления тренировки
        add_frame = tk.LabelFrame(self.root, text="Добавить тренировку", 
                                  font=("Arial", 12, "bold"), 
                                  bg='#f0f0f0', padx=20, pady=15)
        add_frame.pack(pady=10, padx=20, fill='x')
        
        # Дата
        tk.Label(add_frame, text="Дата (ГГГГ-ММ-ДД):", bg='#f0f0f0', 
                font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.date_entry = tk.Entry(add_frame, width=20, font=("Arial", 10))
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Тип тренировки
        tk.Label(add_frame, text="Тип тренировки:", bg='#f0f0f0',
                font=("Arial", 10)).grid(row=0, column=2, padx=5, pady=5, sticky='e')
        self.type_combo = ttk.Combobox(add_frame, values=["Бег", "Плавание", "Велосипед", 
                                                          "Силовая", "Йога", "Растяжка"], 
                                       width=15)
        self.type_combo.grid(row=0, column=3, padx=5, pady=5)
        self.type_combo.set("Бег")
        
        # Длительность
        tk.Label(add_frame, text="Длительность (мин):", bg='#f0f0f0',
                font=("Arial", 10)).grid(row=0, column=4, padx=5, pady=5, sticky='e')
        self.duration_entry = tk.Entry(add_frame, width=10, font=("Arial", 10))
        self.duration_entry.grid(row=0, column=5, padx=5, pady=5)
        
        # Кнопка добавления
        add_btn = tk.Button(add_frame, text="➕ Добавить тренировку", 
                           command=self.add_training,
                           bg='#4CAF50', fg='white', font=("Arial", 10, "bold"),
                           padx=15, pady=5)
        add_btn.grid(row=1, column=0, columnspan=6, pady=10)
        
        # Рамка для фильтрации
        filter_frame = tk.LabelFrame(self.root, text="Фильтрация", 
                                     font=("Arial", 12, "bold"),
                                     bg='#f0f0f0', padx=20, pady=10)
        filter_frame.pack(pady=10, padx=20, fill='x')
        
        # Фильтр по дате
        tk.Label(filter_frame, text="Фильтр по дате (с):", bg='#f0f0f0',
                font=("Arial", 10)).pack(side='left', padx=5)
        self.filter_date = tk.Entry(filter_frame, width=12)
        self.filter_date.pack(side='left', padx=5)
        self.filter_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        tk.Label(filter_frame, text="по:", bg='#f0f0f0',
                font=("Arial", 10)).pack(side='left', padx=5)
        self.filter_date_to = tk.Entry(filter_frame, width=12)
        self.filter_date_to.pack(side='left', padx=5)
        
        # Фильтр по типу
        tk.Label(filter_frame, text="Тип:", bg='#f0f0f0',
                font=("Arial", 10)).pack(side='left', padx=5)
        self.filter_type = ttk.Combobox(filter_frame, values=["Все", "Бег", "Плавание", 
                                                               "Велосипед", "Силовая", "Йога", "Растяжка"], 
                                        width=12)
        self.filter_type.pack(side='left', padx=5)
        self.filter_type.set("Все")
        
        # Кнопка фильтрации
        filter_btn = tk.Button(filter_frame, text="🔍 Применить фильтр", 
                              command=self.filter_trainings,
                              bg='#2196F3', fg='white')
        filter_btn.pack(side='left', padx=10)
        
        # Кнопка сброса фильтра
        reset_btn = tk.Button(filter_frame, text="🔄 Сбросить", 
                              command=self.reset_filter,
                              bg='#FF9800', fg='white')
        reset_btn.pack(side='left', padx=5)
        
        # Таблица для отображения тренировок
        table_frame = tk.LabelFrame(self.root, text="Список тренировок", 
                                    font=("Arial", 12, "bold"),
                                    bg='#f0f0f0', padx=10, pady=10)
        table_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Создание таблицы (Treeview)
        columns = ("Дата", "Тип тренировки", "Длительность (мин)")
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Настройка колонок
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Тип тренировки", text="Тип тренировки")
        self.tree.heading("Длительность (мин)", text="Длительность (мин)")
        
        self.tree.column("Дата", width=120)
        self.tree.column("Тип тренировки", width=150)
        self.tree.column("Длительность (мин)", width=120)
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Кнопка удаления
        delete_btn = tk.Button(self.root, text="🗑 Удалить выбранную тренировку", 
                              command=self.delete_training,
                              bg='#f44336', fg='white', font=("Arial", 10, "bold"),
                              padx=20, pady=5)
        delete_btn.pack(pady=5)
        
        # Обновление таблицы
        self.update_table()
    
    def add_training(self):
        """Добавление тренировки с валидацией"""
        # Получаем данные
        date = self.date_entry.get().strip()
        training_type = self.type_combo.get()
        duration = self.duration_entry.get().strip()
        
        # Валидация даты
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты! Используйте ГГГГ-ММ-ДД")
            return
        
        # Валидация длительности
        if not duration:
            messagebox.showerror("Ошибка", "Введите длительность тренировки!")
            return
        
        try:
            duration_int = int(duration)
            if duration_int <= 0:
                messagebox.showerror("Ошибка", "Длительность должна быть положительным числом!")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Длительность должна быть целым числом!")
            return
        
        # Добавляем тренировку
        training = {
            "date": date,
            "type": training_type,
            "duration": duration_int
        }
        
        self.trainings.append(training)
        self.save_data()
        self.update_table()
        self.duration_entry.delete(0, tk.END)
        
        messagebox.showinfo("Успех", f"Тренировка добавлена!\n{date} - {training_type} - {duration} мин")
    
    def delete_training(self):
        """Удаление выбранной тренировки"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите тренировку для удаления!")
            return
        
        # Получаем индекс выбранной строки
        item = selected[0]
        index = int(self.tree.item(item)['text'])
        
        # Удаляем
        del self.trainings[index]
        self.save_data()
        self.update_table()
        messagebox.showinfo("Успех", "Тренировка удалена!")
    
    def filter_trainings(self):
        """Фильтрация тренировок по дате и типу"""
        filter_date_from = self.filter_date.get().strip()
        filter_date_to = self.filter_date_to.get().strip()
        filter_type = self.filter_type.get()
        
        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Проходим по всем тренировкам
        for i, training in enumerate(self.trainings):
            # Фильтр по дате (с)
            if filter_date_from:
                try:
                    date_obj = datetime.strptime(training['date'], "%Y-%m-%d")
                    date_from = datetime.strptime(filter_date_from, "%Y-%m-%d")
                    if date_obj < date_from:
                        continue
                except:
                    pass
            
            # Фильтр по дате (по)
            if filter_date_to:
                try:
                    date_obj = datetime.strptime(training['date'], "%Y-%m-%d")
                    date_to = datetime.strptime(filter_date_to, "%Y-%m-%d")
                    if date_obj > date_to:
                        continue
                except:
                    pass
            
            # Фильтр по типу
            if filter_type != "Все" and training['type'] != filter_type:
                continue
            
            # Добавляем в таблицу
            self.tree.insert('', 'end', text=str(i), 
                           values=(training['date'], training['type'], f"{training['duration']} мин"))
    
    def reset_filter(self):
        """Сброс фильтрации"""
        self.filter_date.delete(0, tk.END)
        self.filter_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.filter_date_to.delete(0, tk.END)
        self.filter_type.set("Все")
        self.update_table()
    
    def update_table(self):
        """Обновление таблицы (без фильтрации)"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for i, training in enumerate(self.trainings):
            self.tree.insert('', 'end', text=str(i), 
                           values=(training['date'], training['type'], f"{training['duration']} мин"))
    
    def save_data(self):
        """Сохранение данных в JSON"""
        try:
            with open(self.json_file, 'w', encoding='utf-8') as f:
                json.dump(self.trainings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
    
    def load_data(self):
        """Загрузка данных из JSON"""
        if os.path.exists(self.json_file):
            try:
                with open(self.json_file, 'r', encoding='utf-8') as f:
                    self.trainings = json.load(f)
            except Exception as e:
                print(f"Ошибка загрузки: {e}")
                self.trainings = []

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()
