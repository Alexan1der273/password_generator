#version: 0.0.2

import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip  # для копирования в буфер обмена (установите через pip install pyperclip)

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор паролей v0.0.2")
        self.root.geometry("550x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        # Переменные
        self.use_upper = tk.BooleanVar(value=True)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)
        self.password_visible = tk.BooleanVar(value=False)

        self.create_widgets()

    def create_widgets(self):
        # Основной контейнер с отступами
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # ========== Настройки ==========
        settings_frame = tk.LabelFrame(main_frame, text="Настройки пароля", font=("Arial", 10, "bold"), bg="#f0f0f0", fg="#333")
        settings_frame.pack(fill="x", pady=(0, 10))

        # Длина пароля (ползунок + числовое поле)
        length_frame = tk.Frame(settings_frame, bg="#f0f0f0")
        length_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(length_frame, text="Длина:", bg="#f0f0f0", font=("Arial", 10)).pack(side="left")

        self.length_scale = tk.Scale(length_frame, from_=4, to=32, orient="horizontal", command=self.on_length_change, bg="#f0f0f0", highlightthickness=0)
        self.length_scale.set(12)
        self.length_scale.pack(side="left", fill="x", expand=True, padx=10)

        self.length_entry = tk.Entry(length_frame, width=5, font=("Arial", 10), justify="center")
        self.length_entry.insert(0, "12")
        self.length_entry.pack(side="left")

        # Чекбоксы – организованы в 2 колонки для компактности
        chars_frame = tk.Frame(settings_frame, bg="#f0f0f0")
        chars_frame.pack(fill="x", padx=10, pady=5)

        tk.Checkbutton(chars_frame, text="Заглавные (A-Z)", variable=self.use_upper, bg="#f0f0f0", command=self.update_strength_indicator).grid(row=0, column=0, sticky="w", padx=5)
        tk.Checkbutton(chars_frame, text="Строчные (a-z)", variable=self.use_lower, bg="#f0f0f0", command=self.update_strength_indicator).grid(row=0, column=1, sticky="w", padx=5)
        tk.Checkbutton(chars_frame, text="Цифры (0-9)", variable=self.use_digits, bg="#f0f0f0", command=self.update_strength_indicator).grid(row=1, column=0, sticky="w", padx=5)
        tk.Checkbutton(chars_frame, text="Спецсимволы (!@#...)", variable=self.use_symbols, bg="#f0f0f0", command=self.update_strength_indicator).grid(row=1, column=1, sticky="w", padx=5)

        # ========== Генерация ==========
        btn_frame = tk.Frame(main_frame, bg="#f0f0f0")
        btn_frame.pack(fill="x", pady=10)

        generate_btn = tk.Button(btn_frame, text="Сгенерировать пароль", command=self.generate_password, bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), relief="flat", padx=10)
        generate_btn.pack(side="left", expand=True, padx=5)

        clear_btn = tk.Button(btn_frame, text="Очистить", command=self.clear_password, bg="#f44336", fg="white", font=("Arial", 11), relief="flat")
        clear_btn.pack(side="left", expand=True, padx=5)

        # ========== Результат ==========
        result_frame = tk.LabelFrame(main_frame, text="Результат", font=("Arial", 10, "bold"), bg="#f0f0f0", fg="#333")
        result_frame.pack(fill="x", pady=(10, 5))

        # Поле пароля с кнопкой показа/скрытия
        password_container = tk.Frame(result_frame, bg="#f0f0f0")
        password_container.pack(fill="x", padx=10, pady=5)

        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(password_container, textvariable=self.password_var, font=("Courier", 14), justify="center", state="readonly")
        self.password_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.toggle_btn = tk.Button(password_container, text="👁", command=self.toggle_password_visibility, width=3, relief="flat")
        self.toggle_btn.pack(side="left")

        # Кнопка копирования
        copy_btn = tk.Button(result_frame, text="📋 Копировать в буфер", command=self.copy_to_clipboard, bg="#2196F3", fg="white", font=("Arial", 10), relief="flat")
        copy_btn.pack(pady=(0, 10), padx=10, fill="x")

        # Индикатор сложности
        strength_frame = tk.Frame(main_frame, bg="#f0f0f0")
        strength_frame.pack(fill="x", pady=5)

        tk.Label(strength_frame, text="Сложность:", bg="#f0f0f0", font=("Arial", 10)).pack(side="left")
        self.strength_label = tk.Label(strength_frame, text="—", bg="#f0f0f0", font=("Arial", 10, "bold"), fg="gray")
        self.strength_label.pack(side="left", padx=5)

        # Статусная строка
        self.status_var = tk.StringVar()
        self.status_var.set("Готов к работе")
        status_bar = tk.Label(main_frame, textvariable=self.status_var, bd=1, relief="sunken", anchor="w", bg="#e0e0e0", fg="#333", font=("Arial", 9))
        status_bar.pack(fill="x", pady=(10, 0))

    def on_length_change(self, value):
        """Синхронизация ползунка и поля ввода длины."""
        self.length_entry.delete(0, tk.END)
        self.length_entry.insert(0, str(int(float(value))))
        self.update_strength_indicator()

    def update_strength_indicator(self):
        """Обновляет индикатор сложности на основе текущих настроек."""
        try:
            length = int(self.length_entry.get())
        except:
            length = 12

        # Подсчёт возможных символов
        chars_count = 0
        if self.use_upper.get(): chars_count += 26
        if self.use_lower.get(): chars_count += 26
        if self.use_digits.get(): chars_count += 10
        if self.use_symbols.get(): chars_count += 32  # примерно столько спецсимволов

        if chars_count == 0:
            self.strength_label.config(text="Нет выбранных символов", fg="red")
            return

        # Энтропия = log2(количество_символов^длина) = длина * log2(количество_символов)
        import math
        entropy = length * math.log2(chars_count)

        if entropy < 30:
            text, color = "Очень слабый", "#d32f2f"
        elif entropy < 50:
            text, color = "Слабый", "#f57c00"
        elif entropy < 70:
            text, color = "Средний", "#fbc02d"
        elif entropy < 90:
            text, color = "Сильный", "#388e3c"
        else:
            text, color = "Очень сильный", "#00695c"

        self.strength_label.config(text=text, fg=color)

    def toggle_password_visibility(self):
        """Показать/скрыть пароль."""
        if self.password_visible.get():
            self.password_entry.config(show="*")
            self.toggle_btn.config(text="👁")
            self.password_visible.set(False)
        else:
            self.password_entry.config(show="")
            self.toggle_btn.config(text="🙈")
            self.password_visible.set(True)

    def get_character_pool(self):
        char_sets = []
        pool = []

        if self.use_upper.get():
            char_sets.append(string.ascii_uppercase)
            pool.extend(string.ascii_uppercase)
        if self.use_lower.get():
            char_sets.append(string.ascii_lowercase)
            pool.extend(string.ascii_lowercase)
        if self.use_digits.get():
            char_sets.append(string.digits)
            pool.extend(string.digits)
        if self.use_symbols.get():
            symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?/~"
            char_sets.append(symbols)
            pool.extend(symbols)

        return char_sets, pool

    def generate_password(self):
        try:
            length = int(self.length_entry.get())
            if length < 4:
                messagebox.showerror("Ошибка", "Длина должна быть не менее 4 символов")
                return
            if length > 32:
                messagebox.showerror("Ошибка", "Длина не может превышать 32 символа")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную длину")
            return

        char_sets, pool = self.get_character_pool()
        if not char_sets:
            self.status_var.set("Ошибка: выберите хотя бы один тип символов!")
            return

        if length < len(char_sets):
            self.status_var.set(f"Длина должна быть не меньше {len(char_sets)} (по одному символу на тип)")
            return

        guaranteed = [random.choice(chars) for chars in char_sets]
        remaining = length - len(guaranteed)
        extra = [random.choice(pool) for _ in range(remaining)] if remaining > 0 else []

        password_list = guaranteed + extra
        random.shuffle(password_list)
        password = ''.join(password_list)

        self.password_var.set(password)
        self.password_entry.config(state="normal")
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        self.password_entry.config(state="readonly")
        if self.password_visible.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

        self.status_var.set("Пароль успешно сгенерирован!")
        self.update_strength_indicator()

    def clear_password(self):
        self.password_var.set("")
        self.status_var.set("Поле очищено")
        self.password_entry.config(state="normal")
        self.password_entry.delete(0, tk.END)
        self.password_entry.config(state="readonly")

    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password:
            pyperclip.copy(password)
            self.status_var.set("Скопировано в буфер обмена!")
            messagebox.showinfo("Успех", "Пароль скопирован")
        else:
            messagebox.showwarning("Внимание", "Нет пароля для копирования")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()
