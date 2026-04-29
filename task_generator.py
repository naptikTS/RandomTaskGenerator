import tkinter as tk
import random
import json
from datetime import datetime

# Список задач
tasks = [
    {"name": "Прочитать статью", "type": "учёба"},
    {"name": "Сделать зарядку", "type": "спорт"},
    {"name": "Закончить отчёт", "type": "работа"},
    {"name": "Выучить 10 слов", "type": "учёба"},
    {"name": "Пробежка 2 км", "type": "спорт"},
    {"name": "Позвонить маме", "type": "работа"}
]

history = []

# Функция генерации задачи
def generate():
    task = random.choice(tasks)
    time = datetime.now().strftime("%H:%M:%S")
    history.append(f"{time} - {task['name']} [{task['type']}]")
    
    # Обновляем экран
    result_label.config(text=task['name'])
    update_history()
    save_history()

# Обновление списка истории
def update_history():
    history_list.delete(0, tk.END)
    for item in history:
        history_list.insert(tk.END, item)

# Сохранение в файл
def save_history():
    with open("history.json", "w") as f:
        json.dump(history, f)

# Создаём окошко
window = tk.Tk()
window.title("Генератор задач")
window.geometry("500x500")

# Кнопка
btn = tk.Button(window, text="Сгенерировать задачу", command=generate, font=("Arial", 14))
btn.pack(pady=20)

# Результат
result_label = tk.Label(window, text="Нажми кнопку", font=("Arial", 16), fg="blue")
result_label.pack(pady=10)

# Список истории
history_list = tk.Listbox(window, height=15, font=("Arial", 10))
history_list.pack(pady=10, fill="both", expand=True)

# Запускаем программу
window.mainloop()
