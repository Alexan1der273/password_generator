#version:0.0.1 
import tkinter as tk
from tkinter import messagebox
import random
import string
import pyperclip  # для копирования в буфер обмена (установите через pip install pyperclip)

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор паролей")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        # Переменные для хранения состояния чекбоксов
        self.use_upper = tk.BooleanVar(value=True)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)

        # Создание интерфейса
        self.create_widgets()

    def create_widgets(self):
        # Рамка для настроек
        settings_frame = tk.LabelFrame(self.root, text="Настройки пароля", padx=10, pady=10)
        settings_frame.pack(fill="both", padx=10, pady=10)

        # Длина пароля
        tk.Label(settings_frame, text="Длина пароля:").grid(row=0, column=0, sticky="w", pady=5)
        self.length_entry = tk.Entry(settings_frame, width=10)
        self.length_entry.insert(0, "12")
        self.length_entry.grid(row=0, column=1, sticky="w", pady=5)

        # Чекбоксы для выбора символов
        tk.Checkbutton(settings_frame, text="Заглавные буквы (A-Z)", variable=self.use_upper).grid(row=1, column=0, sticky="w")
        tk.Checkbutton(settings_frame, text="Строчные буквы (a-z)", variable=self.use_lower).grid(row=2, column=0, sticky="w")
        tk.Checkbutton(settings_frame, text="Цифры (0-9)", variable=self.use_digits).grid(row=3, column=0, sticky="w")
        tk.Checkbutton(settings_frame, text="Спецсимволы (!@#$%^&*)", variable=self.use_symbols).grid(row=4, column=0, sticky="w")

        # Кнопка генерации
        generate_btn = tk.Button(self.root, text="Сгенерировать пароль", command=self.generate_password, bg="#4CAF50", fg="white", font=("Arial", 12))
        generate_btn.pack(pady=10)

        # Поле для вывода пароля
        tk.Label(self.root, text="Сгенерированный пароль:").pack()
        self.password_var = tk.StringVar()
        password_entry = tk.Entry(self.root, textvariable=self.password_var, font=("Courier", 14), width=30, justify="center")
        password_entry.pack(pady=5)

        # Кнопка копирования
        copy_btn = tk.Button(self.root, text="Копировать в буфер", command=self.copy_to_clipboard, bg="#2196F3", fg="white")
        copy_btn.pack(pady=5)

        # Метка для подсказки
        self.info_label = tk.Label(self.root, text="", fg="red")
        self.info_label.pack()

    def get_character_pool(self):
        """Формирует список доступных символов и список обязательных наборов."""
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
        # Получение длины пароля
        try:
            length = int(self.length_entry.get())
            if length < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную длину пароля (целое число больше 0)")
            return

        # Получаем наборы символов и общий пул
        char_sets, pool = self.get_character_pool()

        # Проверка: выбран хотя бы один тип символов
        if not char_sets:
            self.info_label.config(text="Ошибка: выберите хотя бы один тип символов!")
            return

        # Проверка: минимальная длина не меньше количества выбранных типов
        if length < len(char_sets):
            self.info_label.config(text=f"Длина пароля должна быть не меньше {len(char_sets)} (по одному символу каждого типа).")
            return

        # Гарантированно берём по одному случайному символу из каждого набора
        guaranteed = [random.choice(chars) for chars in char_sets]

        # Оставшееся количество символов
        remaining = length - len(guaranteed)
        # Дозаполняем случайными символами из общего пула
        if remaining > 0:
            extra = [random.choice(pool) for _ in range(remaining)]
        else:
            extra = []

        # Объединяем и перемешиваем
        password_list = guaranteed + extra
        random.shuffle(password_list)
        password = ''.join(password_list)

        # Выводим пароль
        self.password_var.set(password)
        self.info_label.config(text="Пароль успешно сгенерирован!")

    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password:
            pyperclip.copy(password)
            self.info_label.config(text="Пароль скопирован в буфер обмена!")
        else:
            messagebox.showwarning("Внимание", "Нет пароля для копирования. Сначала сгенерируйте пароль.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()
