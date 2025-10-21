import tkinter as tk
from auth_module import AuthWindow
from catalog_module import MainWindow

class LiteratureClubApp:
    def __init__(self):
        self.current_user = None
        
    def on_auth_success(self, user_data):
        """Обработчик успешного завершения авторизации"""
        self.current_user = user_data
        self.show_main_window()
    
    def show_main_window(self):
        """Отображение основного окна приложения"""
        main_window = MainWindow(self.current_user, self.logout)
        main_window.run()
    
    def logout(self):
        """Завершение текущего сеанса пользователя"""
        self.current_user = None
        self.show_auth_window()
    
    def show_auth_window(self):
        """Отображение окна аутентификации"""
        auth_window = AuthWindow(self.on_auth_success)
        auth_window.run()
    
    def run(self):
        """Запуск основного цикла приложения"""
        self.show_auth_window()

if __name__ == "__main__":
    app = LiteratureClubApp()
    app.run()