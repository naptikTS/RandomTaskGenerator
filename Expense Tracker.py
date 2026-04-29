import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Трекер расходов - Expense Tracker")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Данные
        self.expenses = []
        self.json_file = "expenses.json"
        self.categories = ["Еда", "Транспорт", "Развлечения", "Жильё", "Здоровье", 
                          "Одежда", "Связь", "Другое"]
        
        self.load_data()
        self.setup_ui()
    
    def setup_ui(self):
        # Заголовок
        title = tk.Label(self.root, text="💰 Трекер расходов", 
                        font=("Arial", 20, "bold"), 
                        bg='#f0f0f0', fg='#2c3e50')
        title.pack(pady=10)
        
        # ========== Верхняя рамка для добавления расходов ==========
        add_frame = tk.LabelFrame(self.root, text="➕ Добавить расход", 
                                   font=("Arial", 14, "bold"),
                                   bg='#ecf0f1', padx=20, pady=15)
        add_frame.pack(pady=10, padx=20, fill='x')
        
        # Сумма
        tk.Label(add_frame, text="Сумма (₽):", bg='#ecf0f1', 
                font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.amount_entry = tk.Entry(add_frame, width=15, font=("Arial", 12))
        self.amount_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Категория
        tk.Label(add_frame, text="Категория:", bg='#ecf0f1',
                font=("Arial", 12)).grid(row=0, column=2, padx=10, pady=10, sticky='e')
        self.category_combo = ttk.Combobox(add_frame, values=self.categories, 
                                           width=15, font=("Arial", 12))
        self.category_combo.grid(row=0, column=3, padx=10, pady=10)
        self.category_combo.set("Еда")
        
        # Дата
        tk.Label(add_frame, text="Дата (ГГГГ-ММ-ДД):", bg='#ecf0f1',
                font=("Arial", 12)).grid(row=0, column=4, padx=10, pady=10, sticky='e')
        self.date_entry = tk.Entry(add_frame, width=15, font=("Arial", 12))
        self.date_entry.grid(row=0, column=5, padx=10, pady=10)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Кнопка добавления
        add_btn = tk.Button(add_frame, text="➕ Добавить расход", 
                           command=self.add_expense,
                           bg='#27ae60', fg='white', 
                           font=("Arial", 12, "bold"),
                           padx=20, pady=8)
        add_btn.grid(row=1, column=0, columnspan=6, pady=10)
        
        # ========== Рамка для фильтрации ==========
        filter_frame = tk.LabelFrame(self.root, text="🔍 Фильтрация расходов", 
                                      font=("Arial", 14, "bold"),
                                      bg='#ecf0f1', padx=20, pady=10)
        filter_frame.pack(pady=10, padx=20, fill='x')
        
        # Фильтр по дате
        tk.Label(filter_frame, text="Дата с:", bg='#ecf0f1',
                font=("Arial", 11)).grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.filter_date_from = tk.Entry(filter_frame, width=12, font=("Arial", 11))
        self.filter_date_from.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(filter_frame, text="по:", bg='#ecf0f1',
                font=("Arial", 11)).grid(row=0, column=2, padx=5, pady=5, sticky='e')
        self.filter_date_to = tk.Entry(filter_frame, width=12, font=("Arial", 11))
        self.filter_date_to.grid(row=0, column=3, padx=5, pady=5)
        
        # Фильтр по категории
        tk.Label(filter_frame, text="Категория:", bg='#ecf0f1',
                font=("Arial", 11)).grid(row=0, column=4, padx=5, pady=5, sticky='e')
        self.filter_category = ttk.Combobox(filter_frame, values=["Все"] + self.categories, 
                                            width=12, font=("Arial", 11))
        self.filter_category.grid(row=0, column=5, padx=5, pady=5)
        self.filter_category.set("Все")
        
        # Кнопки фильтрации
        filter_btn = tk.Button(filter_frame, text="🔍 Применить фильтр", 
                              command=self.filter_expenses,
                              bg='#3498db', fg='white', font=("Arial", 10, "bold"))
        filter_btn.grid(row=1, column=0, columnspan=3, pady=10, padx=5)
        
        reset_btn = tk.Button(filter_frame, text="🔄 Сбросить фильтр", 
                             command=self.reset_filter,
                             bg='#e67e22', fg='white', font=("Arial", 10, "bold"))
        reset_btn.grid(row=1, column=3, columnspan=3, pady=10, padx=5)
        
        # ========== Рамка для отображения итоговой суммы ==========
        total_frame = tk.Frame(self.root, bg='#2c3e50', padx=10, pady=10)
        total_frame.pack(pady=10, padx=20, fill='x')
        
        self.total_label = tk.Label(total_frame, text="💰 Общая сумма расходов: 0 ₽", 
                                    font=("Arial", 16, "bold"),
                                    bg='#2c3e50', fg='#ffd700')
        self.total_label.pack()
        
        # ========== Таблица расходов ==========
        table_frame = tk.LabelFrame(self.root, text="📋 Список расходов", 
                                     font=("Arial", 14, "bold"),
                                     bg='#ecf0f1', padx=10, pady=10)
        table_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Создание таблицы
        columns = ("ID", "Дата", "Категория", "Сумма (₽)")
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)
        
        self.tree.heading("ID", text="№")
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Категория", text="Категория")
        self.tree.heading("Сумма (₽)", text="Сумма (₽)")
        
        self.tree.column("ID", width=50)
        self.tree.column("Дата", width=120)
        self.tree.column("Категория", width=150)
        self.tree.column("Сумма (₽)", width=120)
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Кнопки управления
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(pady=10)
        
        delete_btn = tk.Button(button_frame, text="🗑 Удалить выбранный расход", 
                              command=self.delete_expense,
                              bg='#e74c3c', fg='white', 
                              font=("Arial", 11, "bold"),
                              padx=15, pady=5)
        delete_btn.pack(side='left', padx=10)
        
        clear_all_btn = tk.Button(button_frame, text="⚠️ Удалить все расходы", 
                                 command=self.clear_all_expenses,
                                 bg='#c0392b', fg='white', 
                                 font=("Arial", 11, "bold"),
                                 padx=15, pady=5)
        clear_all_btn.pack(side='left', padx=10)
        
        # Обновление таблицы
        self.update_table()
    
    def add_expense(self):
        """Добавление расхода с валидацией"""
        # Получаем данные
        amount = self.amount_entry.get().strip()
        category = self.category_combo.get()
        date = self.date_entry.get().strip()
        
        # Валидация суммы
        if not amount:
            messagebox.showerror("Ошибка", "Введите сумму расхода!")
            return
        
        try:
            amount_float = float(amount)
            if amount_float <= 0:
                messagebox.showerror("Ошибка", "Сумма должна быть положительным числом!")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Сумма должна быть числом!")
            return
        
        # Валидация даты
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты! Используйте ГГГГ-ММ-ДД\nПример: 2026-04-29")
            return
        
        # Добавляем расход
        expense = {
            "date": date,
            "category": category,
            "amount": amount_float
        }
        
        self.expenses.append(expense)
        self.save_data()
        self.update_table()
        
        # Очищаем поля
        self.amount_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        messagebox.showinfo("Успех", f"Расход добавлен!\n{date} - {category} - {amount_float} ₽")
    
    def delete_expense(self):
        """Удаление выбранного расхода"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите расход для удаления!")
            return
        
        # Получаем индекс
        item = selected[0]
        index = int(self.tree.item(item)['values'][0]) - 1
        
        # Удаляем
        deleted = self.expenses.pop(index)
        self.save_data()
        self.update_table()
        messagebox.showinfo("Успех", f"Расход удалён!\n{deleted['date']} - {deleted['category']} - {deleted['amount']} ₽")
    
    def clear_all_expenses(self):
        """Удаление всех расходов"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить ВСЕ расходы?"):
            self.expenses = []
            self.save_data()
            self.update_table()
            messagebox.showinfo("Успех", "Все расходы удалены!")
    
    def filter_expenses(self):
        """Фильтрация расходов по дате и категории"""
        filter_from = self.filter_date_from.get().strip()
        filter_to = self.filter_date_to.get().strip()
        filter_cat = self.filter_category.get()
        
        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        filtered_expenses = []
        total = 0
        
        for i, expense in enumerate(self.expenses):
            # Фильтр по дате (начала)
            if filter_from:
                try:
                    date_obj = datetime.strptime(expense['date'], "%Y-%m-%d")
                    date_from = datetime.strptime(filter_from, "%Y-%m-%d")
                    if date_obj < date_from:
                        continue
                except:
                    pass
            
            # Фильтр по дате (конец)
            if filter_to:
                try:
                    date_obj = datetime.strptime(expense['date'], "%Y-%m-%d")
                    date_to = datetime.strptime(filter_to, "%Y-%m-%d")
                    if date_obj > date_to:
                        continue
                except:
                    pass
            
            # Фильтр по категории
            if filter_cat != "Все" and expense['category'] != filter_cat:
                continue
            
            filtered_expenses.append(expense)
            total += expense['amount']
        
        # Отображаем отфильтрованные расходы
        for i, expense in enumerate(filtered_expenses, 1):
            self.tree.insert('', 'end', 
                           values=(i, expense['date'], expense['category'], f"{expense['amount']:.2f}"))
        
        # Обновляем сумму
        self.total_label.config(text=f"💰 Сумма за период: {total:.2f} ₽")
        
        count = len(filtered_expenses)
        messagebox.showinfo("Результат", f"Найдено расходов: {count}\nОбщая сумма: {total:.2f} ₽")
    
    def reset_filter(self):
        """Сброс фильтрации"""
        self.filter_date_from.delete(0, tk.END)
        self.filter_date_to.delete(0, tk.END)
        self.filter_category.set("Все")
        self.update_table()
    
    def update_table(self):
        """Обновление таблицы (без фильтрации)"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        total = 0
        for i, expense in enumerate(self.expenses, 1):
            self.tree.insert('', 'end', 
                           values=(i, expense['date'], expense['category'], f"{expense['amount']:.2f}"))
            total += expense['amount']
        
        self.total_label.config(text=f"💰 Общая сумма всех расходов: {total:.2f} ₽")
    
    def save_data(self):
        """Сохранение данных в JSON"""
        try:
            with open(self.json_file, 'w', encoding='utf-8') as f:
                json.dump(self.expenses, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
    
    def load_data(self):
        """Загрузка данных из JSON"""
        if os.path.exists(self.json_file):
            try:
                with open(self.json_file, 'r', encoding='utf-8') as f:
                    self.expenses = json.load(f)
            except Exception as e:
                print(f"Ошибка загрузки: {e}")
                self.expenses = []

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
