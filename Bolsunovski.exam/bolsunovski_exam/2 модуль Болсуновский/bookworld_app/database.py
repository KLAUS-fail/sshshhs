import sqlite3
import os
from typing import List, Dict, Optional

class DatabaseManager:
    def __init__(self, db_path: str = "literature_club.db"):
        self.db_path = db_path
    
    def get_connection(self):
        """Установление подключения к базе данных"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def authenticate_user(self, login: str, password: str) -> Optional[Dict]:
        """Проверка учетных данных пользователя"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT user_id, role, full_name FROM users WHERE login = ? AND password = ?",
                    (login, password)
                )
                result = cursor.fetchone()
                if result:
                    return {
                        'user_id': result[0],
                        'role': result[1],
                        'full_name': result[2]
                    }
        except Exception as e:
            print(f"Произошла ошибка при проверке учетных данных: {e}")
        return None
    
    def get_all_books(self, search_query: str = None) -> List[Dict]:
        """Получение списка книг с поддержкой поиска"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                if search_query and search_query.strip():
                    # Поиск с учетом регистра
                    query = """
                        SELECT * FROM books 
                        WHERE LOWER(title) LIKE LOWER(?) 
                           OR LOWER(author) LIKE LOWER(?)
                           OR LOWER(genre) LIKE LOWER(?)
                        ORDER BY title
                    """
                    search_pattern = f'%{search_query.strip()}%'
                    cursor.execute(query, (search_pattern, search_pattern, search_pattern))
                else:
                    query = "SELECT * FROM books ORDER BY title"
                    cursor.execute(query)
                
                # Получение названий столбцов
                columns = [description[0] for description in cursor.description]
                books = []
                
                for row in cursor.fetchall():
                    book_dict = {}
                    for i, column in enumerate(columns):
                        book_dict[column] = row[i]
                    books.append(book_dict)
                
                print(f" Поисковый запрос '{search_query}': найдено {len(books)} книг")
                return books
                
        except Exception as e:
            print(f" Ошибка при загрузке списка книг: {e}")
            return []
    
    def get_book_by_article(self, article: str) -> Optional[Dict]:
        """Получение информации о книге по уникальному артикулу"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM books WHERE article = ?", (article,))
                
                columns = [description[0] for description in cursor.description]
                result = cursor.fetchone()
                
                if result:
                    book_dict = {}
                    for i, column in enumerate(columns):
                        book_dict[column] = result[i]
                    return book_dict
                return None
                
        except Exception as e:
            print(f"Ошибка при получении данных о книге: {e}")
            return None