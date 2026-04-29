import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

class TaskGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных задач")
        self.root.geometry("650x750")
        self.root.configure(bg='#f0f0f0')
        
        # Предопределённые задачи
        self.default_tasks = [
            {"name": "Прочитать статью по Python", "type": "учёба"},
            {"name": "Сделать зарядку 15 минут", "type": "спорт"},
            {"name": "Закончить отчёт по проекту", "type": "работа"},
            {"name": "Выучить 10 новых слов", "type": "учёба"},
            {"name": "Пробежка 3 км", "type": "спорт"},
            {"name": "Позвонить клиенту", "type": "работа"},
            {"name": "Посмотреть вебинар", "type": "учёба"},
            {"name": "Отжимания 3 подхода", "type": "спорт"},
            {"name": "Составить план на неделю", "type": "работа"}
        ]
        
        self.tasks = self.default_tasks.copy()
        self.history = []
        self.json_file = "task_history.json"
        
        self.load_history()
        self.setup_ui()
        
    def setup_ui(self):
        # Заголовок
        title = tk.Label(self.root, text="🎲 Генератор случайных задач", 
                        font=("Arial", 18, "bold"), bg='#f0f0f0', fg='#333')
        title.pack(pady=15)
        
        # Кнопка генерации
        self.generate_btn = tk.Button(self.root, text="Сгенерировать задачу", 
                                     command=self.generate_task,
                                     font=("Arial", 14, "bold"), 
                                     bg='#4CAF50', fg='white',
                                     padx=30, pady=12,
                                     relief='raised', bd=3)
        self.generate_btn.pack(pady=15)
        
        # Отображение задачи
        self.task_display = tk.Label(self.root, text="⚡ Нажмите кнопку ⚡",
                                     font=("Arial", 14), 
                                     bg='#ffffff', fg='#2196F3',
                                     relief='sunken', padx=20, pady=20,
                                     wraplength=500)
        self.task_display.pack(pady=10, padx=20, fill='x')
        
        # Фильтрация
        filter_frame = tk.LabelFrame(self.root, text="Фильтр по типу", 
                                     font=("Arial", 11, "bold"),
                                     bg='#f0f0f0', padx=10, pady=10)
        filter_frame.pack(pady=10, padx=20, fill='x')
        
        self.filter_var = tk.StringVar(value="все")
        filters = [("📚 Все", "все"), ("📖 Учёба", "учёба"), 
                   ("🏃 Спорт", "спорт"), ("💼 Работа", "работа")]
        
        for text, value in filters:
            rb = tk.Radiobutton(filter_frame, text=text, variable=self.filter_var,
                               value=value, command=self.filter_history,
                               bg='#f0f0f0', font=("Arial", 10))
            rb.pack(side='left', padx=10)
        
        # Добавление задачи
        add_frame = tk.LabelFrame(self.root, text="Добавить новую задачу",
                                  font=("Arial", 11, "bold"),
                                  bg='#f0f0f0', padx=10, pady=10)
        add_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(add_frame, text="Название:", bg='#f0f0f0', 
                font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5)
        self.task_entry = tk.Entry(add_frame, width=35, font=("Arial", 10))
        self.task_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(add_frame, text="Тип:", bg='#f0f0f0',
                font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=5)
        self.type_combo = ttk.Combobox(add_frame, values=["учёба", "спорт", "работа"],
                                       width=32)
        self.type_combo.grid(row=1, column=1, padx=5, pady=5)
        self.type_combo.set("учёба")
        
        add_btn = tk.Button(add_frame, text="➕ Добавить", command=self.add_task,
                           bg='#2196F3', fg='white', font=("Arial", 10, "bold"),
                           padx=20)
        add_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # История
        history_frame = tk.LabelFrame(self.root, text="📜 История задач",
                                      font=("Arial", 11, "bold"),
                                      bg='#f0f0f0', padx=10, pady=10)
        history_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(history_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.history_listbox = tk.Listbox(history_frame, 
                                          yscrollcommand=scrollbar.set,
                                          font=("Arial", 9),
                                          height=10,
                                          bg='#ffffff')
        self.history_listbox.pack(fill='both', expand=True)
        scrollbar.config(command=self.history_listbox.yview)
        
        # Кнопка очистки
        clear_btn = tk.Button(self.root, text="🗑 Очистить историю", 
                             command=self.clear_history,
                             bg='#f44336', fg='white', 
                             font=("Arial", 10, "bold"),
                             padx=20, pady=5)
        clear_btn.pack(pady=10)
        
        self.update_history_display()
    
    def generate_task(self):
        if not self.tasks:
            messagebox.showwarning("Ошибка", "Нет доступных задач!")
            return
        
        task = random.choice(self.tasks)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        history_entry = {
            "time": timestamp,
            "task": task["name"],
            "type": task["type"]
        }
        
        self.history.append(history_entry)
        self.task_display.config(text=f"🎉 {task['name']} 🎉")
        self.save_history()
        self.update_history_display()
    
    def add_task(self):
        task_name = self.task_entry.get().strip()
        task_type = self.type_combo.get()
        
        if not task_name:
            messagebox.showerror("Ошибка", "Название задачи не может быть пустым!")
            return
        
        for task in self.tasks:
            if task["name"].lower() == task_name.lower():
                messagebox.showwarning("Внимание", "Такая задача уже есть!")
                return
        
        self.tasks.append({"name": task_name, "type": task_type})
        self.task_entry.delete(0, tk.END)
        messagebox.showinfo("Успех", f"Задача '{task_name}' добавлена!")
    
    def filter_history(self):
        self.update_history_display()
    
    def update_history_display(self):
        self.history_listbox.delete(0, tk.END)
        filter_type = self.filter_var.get()
        
        for entry in self.history:
            if filter_type == "все" or entry["type"] == filter_type:
                display_text = f"[{entry['time']}] {entry['task']} ({entry['type']})"
                self.history_listbox.insert(tk.END, display_text)
    
    def save_history(self):
        try:
            with open(self.json_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def load_history(self):
        if os.path.exists(self.json_file):
            try:
                with open(self.json_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            except:
                self.history = []
    
    def clear_history(self):
        if messagebox.askyesno("Подтверждение", "Очистить всю историю?"):
            self.history = []
            self.save_history()
            self.update_history_display()
            self.task_display.config(text="История очищена")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskGenerator(root)
    root.mainloop()
