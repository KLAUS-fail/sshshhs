import tkinter as tk
from tkinter import messagebox
from database import DatabaseManager

class AuthWindow:
    def __init__(self, on_success_callback):
        self.on_success_callback = on_success_callback
        self.db = DatabaseManager()
        
        self.window = tk.Tk()
        self.window.title("Литературный Клуб - Вход в систему")
        self.window.geometry("400x300")
        self.window.resizable(False, False)
        
        self._create_interface()
    
    def _create_interface(self):
        """Создание элементов интерфейса для авторизации"""
        # Заголовок
        title_label = tk.Label(
            self.window, 
            text="Литературный Клуб", 
            font=("Arial", 20, "bold"),
            fg="#2E86AB"
        )
        title_label.pack(pady=20)
        
        # Поле для ввода логина
        tk.Label(self.window, text="Имя пользователя:").pack(anchor="w", padx=50)
        self.login_entry = tk.Entry(self.window, width=30)
        self.login_entry.pack(pady=5, padx=50)
        
        # Поле для ввода пароля
        tk.Label(self.window, text="Пароль:").pack(anchor="w", padx=50)
        self.password_entry = tk.Entry(self.window, width=30, show="*")
        self.password_entry.pack(pady=5, padx=50)
        
        # Кнопка авторизации
        login_button = tk.Button(
            self.window,
            text="Войти в систему",
            command=self._perform_login,
            bg="#2E86AB",
            fg="white",
            width=15
        )
        login_button.pack(pady=10)
        
        # Кнопка для гостевого доступа
        guest_button = tk.Button(
            self.window,
            text="Продолжить как гость",
            command=self._guest_access,
            bg="#A23B72",
            fg="white",
            width=15
        )
        guest_button.pack(pady=5)
        
        # Справочная информация
        hint_label = tk.Label(
            self.window,
            text="Для тестового входа используйте:\nЛогин: a.belov@example.com Пароль: Fh9jQw",
            font=("Arial", 8),
            fg="gray"
        )
        hint_label.pack(pady=10)
    
    def _perform_login(self):
        """Выполнение процедуры входа в систему"""
        username = self.login_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Ошибка ввода", "Необходимо указать имя пользователя и пароль")
            return
        
        user_info = self.db.authenticate_user(username, password)
        if user_info:
            self.window.destroy()
            self.on_success_callback(user_info)
        else:
            messagebox.showerror("Ошибка авторизации", "Введены неверные учетные данные")
    
    def _guest_access(self):
        """Авторизация в режиме гостя"""
        self.window.destroy()
        self.on_success_callback({
            'user_id': None,
            'role': 'Гость',
            'full_name': 'Гость'
        })
    
    def start(self):
        """Запуск основного цикла окна авторизации"""
        self.window.mainloop()