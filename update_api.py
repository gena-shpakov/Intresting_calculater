import tkinter as tk
from tkinter import messagebox
import requests
import os
import sys
import subprocess

CURRENT_VERSION = "1.0.0"
API_URL = "https://raw.githubusercontent.com/gena-shpakov/Intresting_calculater/main/check_update.json"

def check_for_update():
    try:
        response = requests.get(API_URL, timeout=5)
        data = response.json()

        latest_version = data.get("version")
        changelog = data.get("changelog", "")
        download_url = data.get("download_url")

        if not latest_version or not download_url:
            messagebox.showerror("Помилка", "Файл оновлення некоректний.")
            return

        if latest_version > CURRENT_VERSION:
            answer = messagebox.askyesno(
                "Доступне оновлення",
                f"Знайдено нову версію: {latest_version}\n\nЗміни:\n{changelog}\n\nОновити зараз?"
            )
            if answer:
                download_and_install(download_url)
        else:
            messagebox.showinfo("Оновлення", "У вас вже найновіша версія.")

    except Exception as e:
        messagebox.showerror("Помилка", f"Не вдалося перевірити оновлення:\n{e}")

def download_and_install(url):
    try:
        filename = os.path.basename(url)

        messagebox.showinfo("Завантаження", "Починаю завантаження оновлення...")

        r = requests.get(url, stream=True)
        total_size = int(r.headers.get('content-length', 0))

        with open(filename, 'wb') as f:
            downloaded = 0
            for chunk in r.iter_content(1024):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)

        messagebox.showinfo("Оновлення", "Оновлення завантажено. Запускаю установку...")
        
        subprocess.Popen([filename])

        sys.exit()

    except Exception as e:
        messagebox.showerror("Помилка", f"Не вдалося завантажити оновлення:\n{e}")

# ---------------- ТЕСТ ----------------
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw() 
    check_for_update()
