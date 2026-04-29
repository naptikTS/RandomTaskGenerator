import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os
from datetime import datetime

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор паролей")
        self.root.geometry("750x650")
        self.root.configure(bg='#2c3e50')
        
        # История паролей
        self.history = []
        self.json_file = "passwords_history.json"
        
        self.load_history()
        self.setup_ui()
    
    def setup_ui(self):
        # Заголовок
        title = tk.Label(self.root, text="🔐 Генератор паролей", 
                        font=("Arial", 20, "bold"), 
                        bg='#2c3e50', fg='white')
        title.pack(pady=15)
        
        # Рамка настроек
        settings_frame = tk.LabelFrame(self.root, text="Настройки пароля", 
                                       font=("Arial", 14, "bold"),
                                       bg='#ecf0f1', fg='#2c3e50', 
                                       padx=20, pady=15)
        settings_frame.pack(pady=10, padx=20, fill='x')
        
        # Ползунок длины пароля
        tk.Label(settings_frame, text="Длина пароля:", 
                bg='#ecf0f1', font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
        
        self.length_var = tk.IntVar(value=12)
        self.length_slider = tk.Scale(settings_frame, from_=4, to=32, 
                                      orient='horizontal', variable=self.length_var,
                                      length=300, showvalue=0)
        self.length_slider.grid(row=0, column=1, padx=10, pady=10)
        
        self.length_label = tk.Label(settings_frame, text="12", 
                                     bg='#ecf0f1', font=("Arial", 12, "bold"),
                                     width=5)
        self.length_label.grid(row=0, column=2, padx=10, pady=10)
        self.length_slider.configure(command=self.update_length_label)
        
        # Чекбоксы для выбора символов
        tk.Label(settings_frame, text="Включить:", 
                bg='#ecf0f1', font=("Arial", 12, "bold")).grid(row=1, column=0, padx=10, pady=10, sticky='w')
        
        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_lowercase = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)
        
        tk.Checkbutton(settings_frame, text="Заглавные буквы (A-Z)", 
                      variable=self.use_uppercase, bg='#ecf0f1',
                      font=("Arial", 10)).grid(row=1, column=1, padx=10, pady=5, sticky='w')
        
        tk.Checkbutton(settings_frame, text="Строчные буквы (a-z)", 
                      variable=self.use_lowercase, bg='#ecf0f1',
                      font=("Arial", 10)).grid(row=2, column=1, padx=10, pady=5, sticky='w')
        
        tk.Checkbutton(settings_frame, text="Цифры (0-9)", 
                      variable=self.use_digits, bg='#ecf0f1',
                      font=("Arial", 10)).grid(row=3, column=1, padx=10, pady=5, sticky='w')
        
        tk.Checkbutton(settings_frame, text="Спецсимволы (!@#$%^&*)", 
                      variable=self.use_symbols, bg='#ecf0f1',
                      font=("Arial", 10)).grid(row=4, column=1, padx=10, pady=5, sticky='w')
        
        # Кнопка генерации
        generate_btn = tk.Button(self.root, text="🎲 Сгенерировать пароль", 
                                command=self.generate_password,
                                font=("Arial", 14, "bold"),
                                bg='#27ae60', fg='white',
                                padx=30, pady=12)
        generate_btn.pack(pady=15)
        
        # Отображение сгенерированного пароля
        self.password_display = tk.Text(self.root, height=3, width=50,
                                        font=("Courier", 14),
                                        relief='sunken', bd=3,
                                        bg='white', fg='#2c3e50')
        self.password_display.pack(pady=10, padx=20, fill='x')
        
        # Кнопка копирования
        copy_btn = tk.Button(self.root, text="📋 Скопировать пароль", 
                            command=self.copy_password,
                            font=("Arial", 11),
                            bg='#3498db', fg='white',
                            padx=20, pady=5)
        copy_btn.pack(pady=5)
        
        # История паролей
        history_frame = tk.LabelFrame(self.root, text="📜 История паролей", 
                                      font=("Arial", 14, "bold"),
                                      bg='#ecf0f1', fg='#2c3e50',
                                      padx=10, pady=10)
        history_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Таблица для истории
        columns = ("Дата", "Пароль", "Длина", "Сложность")
        self.tree = ttk.Treeview(history_frame, columns=columns, show='headings', height=8)
        
        self.tree.heading("Дата", text="Дата создания")
        self.tree.heading("Пароль", text="Пароль")
        self.tree.heading("Длина", text="Длина")
        self.tree.heading("Сложность", text="Сложность")
        
        self.tree.column("Дата", width=150)
        self.tree.column("Пароль", width=200)
        self.tree.column("Длина", width=80)
        self.tree.column("Сложность", width=100)
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(history_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Кнопка очистки истории
        clear_btn = tk.Button(self.root, text="🗑 Очистить историю", 
                             command=self.clear_history,
                             bg='#e74c3c', fg='white', 
                             font=("Arial", 11, "bold"),
                             padx=20, pady=5)
        clear_btn.pack(pady=10)
        
        # Обновление таблицы
        self.update_history_table()
    
    def update_length_label(self, value):
        """Обновление отображения длины пароля"""
        self.length_label.config(text=str(int(float(value))))
    
    def generate_password(self):
        """Генерация пароля согласно настройкам"""
        # Проверка, что выбран хотя бы один тип символов
        if not (self.use_uppercase.get() or self.use_lowercase.get() or 
                self.use_digits.get() or self.use_symbols.get()):
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов!")
            return
        
        length = self.length_var.get()
        
        # Валидация длины
        if length < 4:
            messagebox.showerror("Ошибка", "Длина пароля должна быть не менее 4 символов!")
            return
        if length > 32:
            messagebox.showerror("Ошибка", "Длина пароля должна быть не более 32 символов!")
            return
        
        # Формируем набор символов
        characters = ""
        if self.use_uppercase.get():
            characters += string.ascii_uppercase
        if self.use_lowercase.get():
            characters += string.ascii_lowercase
        if self.use_digits.get():
            characters += string.digits
        if self.use_symbols.get():
            characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Генерация пароля
        password_chars = []
        for _ in range(length):
            password_chars.append(random.choice(characters))
        
        # Перемешиваем для случайности
        random.shuffle(password_chars)
        password = ''.join(password_chars)
        
        # Отображаем пароль
        self.password_display.delete(1.0, tk.END)
        self.password_display.insert(1.0, password)
        
        # Сохраняем в историю
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Определяем сложность
        complexity = self.calculate_complexity(password)
        
        history_entry = {
            "time": timestamp,
            "password": password,
            "length": length,
            "complexity": complexity
        }
        
        self.history.append(history_entry)
        self.save_history()
        self.update_history_table()
        
        messagebox.showinfo("Успех", f"Пароль сгенерирован!\nДлина: {length} символов\nСложность: {complexity}")
    
    def calculate_complexity(self, password):
        """Расчёт сложности пароля"""
        score = 0
        if any(c.isupper() for c in password):
            score += 1
        if any(c.islower() for c in password):
            score += 1
        if any(c.isdigit() for c in password):
            score += 1
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            score += 1
        if len(password) >= 12:
            score += 1
        
        if score <= 2:
            return "Слабый"
        elif score <= 4:
            return "Средний"
        else:
            return "Сильный"
    
    def copy_password(self):
        """Копирование пароля в буфер обмена"""
        password = self.password_display.get(1.0, tk.END).strip()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена!")
        else:
            messagebox.showwarning("Внимание", "Сначала сгенерируйте пароль!")
    
    def update_history_table(self):
        """Обновление таблицы истории"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for entry in self.history:
            # Маскируем пароль для отображения
            masked_password = entry['password'][:3] + '***' + entry['password'][-3:] if len(entry['password']) > 6 else '***'
            self.tree.insert('', 'end', 
                           values=(entry['time'], masked_password, 
                                  entry['length'], entry['complexity']))
    
    def clear_history(self):
        """Очистка истории"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить историю паролей?"):
            self.history = []
            self.save_history()
            self.update_history_table()
            messagebox.showinfo("Успех", "История очищена!")
    
    def save_history(self):
        """Сохранение истории в JSON"""
        try:
            with open(self.json_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
    
    def load_history(self):
        """Загрузка истории из JSON"""
        if os.path.exists(self.json_file):
            try:
                with open(self.json_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            except Exception as e:
                print(f"Ошибка загрузки: {e}")
                self.history = []

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()
