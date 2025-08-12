import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import random
import os
import requests

# --- Налаштування ---
CURRENT_VERSION = "1.0.0"
API_URL = "https://raw.githubusercontent.com/gena-shpakov/Intresting_calculater/main/check_update.json"

PRIMARY_COLOR = "#4CAF50"  # Зелений Material
SECONDARY_COLOR = "#2E7D32"
TEXT_COLOR = "#FFFFFF"
FONT_MAIN = ("Segoe UI", 12)

# --- Перевірка оновлення через API ---
def check_for_update():
    try:
        response = requests.get(API_URL, timeout=5)
        data = response.json()

        if data["version"] != CURRENT_VERSION:
            messagebox.showinfo(
                "Доступне оновлення",
                f"Нова версія: {data['version']}\n\n"
                f"Зміни:\n{data['changelog']}\n\n"
                f"Завантажити: {data['download_url']}"
            )
        else:
            messagebox.showinfo("Оновлень немає", "У вас встановлена остання версія.")
    except Exception as e:
        messagebox.showerror("Помилка", f"Не вдалося перевірити оновлення:\n{e}")

# --- Логіка вибору файлу ---
def choose_file():
    file_path = filedialog.askopenfilename(title="Виберіть файл для видалення")
    if file_path:
        generate_task(file_path)

# --- Генерація завдання ---
def generate_task(file_path):
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operation = random.choice(["+", "*"])
    correct_answer = num1 + num2 if operation == "+" else num1 * num2

    task_window = tk.Toplevel(root)
    task_window.title("Перевірка перед видаленням")
    task_window.geometry("350x180")
    task_window.resizable(True, True)

    task_window.columnconfigure(0, weight=1)
    task_window.rowconfigure([0, 1, 2], weight=1)

    ttk.Label(task_window, text=f"Обчисліть: {num1} {operation} {num2} = ?", font=FONT_MAIN).grid(row=0, column=0, pady=10, sticky="nsew")
    answer_entry = ttk.Entry(task_window, font=FONT_MAIN)
    answer_entry.grid(row=1, column=0, pady=5, padx=15, sticky="nsew")

    def check_answer():
        try:
            user_answer = int(answer_entry.get())
            if user_answer == correct_answer:
                confirm_deletion(file_path, task_window)
            else:
                messagebox.showerror("Помилка", "Невдала спроба видалення файлу!")
                task_window.destroy()
        except ValueError:
            messagebox.showerror("Помилка", "Введіть число!")

    create_button(task_window, "Перевірити", check_answer).grid(row=2, column=0, pady=10, padx=15, sticky="nsew")

# --- Підтвердження видалення ---
def confirm_deletion(file_path, window):
    result = messagebox.askyesno("Підтвердження", f"Ви дійсно хочете видалити файл?\n{file_path}")
    if result:
        try:
            os.remove(file_path)
            messagebox.showinfo("Успіх", "Файл успішно видалено!")
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося видалити файл: {e}")
    else:
        messagebox.showinfo("Скасовано", "Видалення скасовано.")
    window.destroy()

# --- Підказка ---
def show_hint():
    hint_text = (
        "Кнопка 'Обрати файл' — відкриває вікно для вибору файлу, який ви хочете видалити.\n\n"
        "Після вибору файлу з'явиться математичне завдання для підтвердження видалення.\n\n"
        "Кнопка 'Перевірити оновлення' — перевіряє через інтернет чи є нові версії програми.\n\n"
        "Якщо ви правильно розв'яжете приклад, файл буде видалено."
    )
    messagebox.showinfo("Підказка", hint_text)

# --- Кнопка з сучасним виглядом ---
def create_button(parent, text, command):
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        bg=PRIMARY_COLOR,
        fg=TEXT_COLOR,
        font=FONT_MAIN,
        relief="flat",
        activebackground=SECONDARY_COLOR,
        activeforeground=TEXT_COLOR,
        cursor="hand2"
    )
    return btn

# --- Інтерфейс ---
root = tk.Tk()
root.title("Калькулятор для видалення файлів")
root.geometry("500x300")
root.resizable(True, True)

root.columnconfigure(0, weight=1)
root.rowconfigure([0, 1, 2, 3], weight=1)

ttk.Label(root, text="Натисніть кнопку, щоб обрати файл для видалення", font=("Segoe UI", 13, "bold")).grid(row=0, column=0, pady=20, sticky="nsew")
create_button(root, "Обрати файл", choose_file).grid(row=1, column=0, pady=5, padx=20, sticky="nsew")
create_button(root, "Перевірити оновлення", check_for_update).grid(row=2, column=0, pady=5, padx=20, sticky="nsew")
create_button(root, "Підказка", show_hint).grid(row=3, column=0, pady=5, padx=20, sticky="nsew")

root.mainloop()
