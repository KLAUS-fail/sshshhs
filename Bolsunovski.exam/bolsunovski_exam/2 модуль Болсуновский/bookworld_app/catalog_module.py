import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from database import DatabaseManager

class MainWindow:
    def __init__(self, user_data, logout_callback):
        self.user_data = user_data
        self.logout_callback = logout_callback
        self.db = DatabaseManager()
        
        self.window = tk.Tk()
        self.window.title("Литературный Клуб - Каталог произведений")
        self.window.geometry("1000x700")
        self.window.configure(bg="#f5f5f5")
        
        # Кэш для хранения изображений книг
        self.book_images = {}
        self._load_book_images()
        
        self._create_interface()
        self._load_books()
    
    def _load_book_images(self):
        """Загрузка изображений обложек книг"""
        try:
            # Загрузка логотипа приложения
            if os.path.exists("resources/logo.png"):
                logo_image = Image.open("resources/logo.png")
                logo_image = logo_image.resize((150, 50), Image.Resampling.LANCZOS)
                self.logo_image = ImageTk.PhotoImage(logo_image)
            else:
                self.logo_image = None
            
            # Загрузка изображений обложек (1.png, 2.png, ..., 10.png)
            for i in range(1, 11):
                image_path = f"resources/{i}.png"
                if os.path.exists(image_path):
                    book_image = Image.open(image_path)
                    book_image = book_image.resize((100, 150), Image.Resampling.LANCZOS)
                    self.book_images[str(i)] = ImageTk.PhotoImage(book_image)
            
            # Загрузка изображения-заглушки для отсутствующих обложек
            if os.path.exists("resources/placeholder.png"):
                placeholder_image = Image.open("resources/placeholder.png")
                placeholder_image = placeholder_image.resize((100, 150), Image.Resampling.LANCZOS)
                self.placeholder_image = ImageTk.PhotoImage(placeholder_image)
            else:
                self.placeholder_image = None
                
        except Exception as e:
            print(f"Произошла ошибка при загрузке изображений: {e}")
            self.logo_image = None
            self.placeholder_image = None
    
    def _get_book_image(self, book_article):
        """Получение изображения книги по артикулу"""
        # Соответствие артикулов книг номерам изображений
        article_to_image_map = {
            'B112F4': '1',  # Мастер и Маргарита
            'F635R4': '2',  # 1984
            'H782T5': '3',  # Преступление и наказание
            'G783F5': '4',  # Три товарища
            'J384T6': '5',  # Маленький принц
            'D572U8': '6',  # Шерлок Холмс
            'F572H7': '7',  # Гарри Поттер
            'D329H3': '8',  # Убийство в Восточном экспрессе
            'B320R5': '9',  # Война и мир
            'G432E4': '10', # Алхимик
            'S213E3': None, # Портрет Дориана Грея (изображение отсутствует)
            'E482R4': None, # Над пропастью во ржи (изображение отсутствует)
            'S634B5': None, # Игра Эндера (изображение отсутствует)
            'K345R4': None, # Автостопом по галактике (изображение отсутствует)
            'O754F4': None  # Цветы для Элджернона (изображение отсутствует)
        }
        
        image_key = article_to_image_map.get(book_article)
        if image_key and image_key in self.book_images:
            return self.book_images[image_key]
        else:
            return self.placeholder_image
    
    def _create_interface(self):
        """Создание пользовательского интерфейса главного окна"""
        # Верхняя панель с навигацией
        header_frame = tk.Frame(self.window, bg="#2E86AB", height=80)
        header_frame.pack(fill="x", padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        # Логотип в левой части
        if self.logo_image:
            logo_label = tk.Label(header_frame, image=self.logo_image, bg="#2E86AB")
            logo_label.pack(side="left", padx=10, pady=10)
        else:
            logo_label = tk.Label(
                header_frame, 
                text="Литературный Клуб", 
                font=("Arial", 16, "bold"), 
                fg="white", 
                bg="#2E86AB"
            )
            logo_label.pack(side="left", padx=10, pady=10)
        
        # Блок с информацией о пользователе в правой части
        user_info_frame = tk.Frame(header_frame, bg="#2E86AB")
        user_info_frame.pack(side="right", padx=10, pady=10)
        
        user_name_label = tk.Label(
            user_info_frame, 
            text=f"{self.user_data['full_name']} ({self.user_data['role']})",
            font=("Arial", 10),
            fg="white",
            bg="#2E86AB"
        )
        user_name_label.pack(anchor="e")
        
        logout_button = tk.Button(
            user_info_frame,
            text="Завершить сеанс",
            command=self.logout_callback,
            bg="#A23B72",
            fg="white",
            font=("Arial", 8)
        )
        logout_button.pack(anchor="e", pady=(5, 0))
        
        # Панель поиска (доступна для клиентов, менеджеров и администраторов)
        if self.user_data['role'] != 'Гость':
            search_frame = tk.Frame(self.window, bg="#f5f5f5")
            search_frame.pack(fill="x", padx=20, pady=10)
            
            tk.Label(
                search_frame, 
                text="Поиск произведений:", 
                font=("Arial", 10),
                bg="#f5f5f5"
            ).pack(side="left")
            
            self.search_entry = tk.Entry(search_frame, width=40)
            self.search_entry.pack(side="left", padx=10)
            self.search_entry.bind("<KeyRelease>", self._on_search_change)
            
            search_button = tk.Button(
                search_frame,
                text="Выполнить поиск",
                command=self._perform_search,
                bg="#2E86AB",
                fg="white"
            )
            search_button.pack(side="left", padx=5)
        
        # Контейнер для отображения списка книг
        self.books_frame = tk.Frame(self.window, bg="#f5f5f5")
        self.books_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Элементы для прокрутки содержимого
        self.canvas = tk.Canvas(self.books_frame, bg="#f5f5f5")
        self.scrollbar = ttk.Scrollbar(self.books_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f5f5f5")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
    
    def _load_books(self, search_query: str = None):
        """Загрузка и отображение списка книг"""
        books = self.db.get_all_books(search_query)
        
        # Очистка предыдущего содержимого
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        if not books:
            no_books_label = tk.Label(
                self.scrollable_frame,
                text="Книги по вашему запросу не найдены",
                font=("Arial", 14),
                bg="#f5f5f5",
                fg="gray"
            )
            no_books_label.pack(pady=50)
            return
        
        # Отображение книг в виде сетки
        row_frame = None
        for i, book in enumerate(books):
            if i % 3 == 0:  # По 3 книги в каждой строке
                row_frame = tk.Frame(self.scrollable_frame, bg="#f5f5f5")
                row_frame.pack(fill="x", pady=10)
            
            self._create_book_card(row_frame, book)
    
    def _create_book_card(self, parent, book):
        """Создание карточки для отображения информации о книге"""
        # Основной контейнер для карточки книги
        book_bg_color = "#ADD8E6" if book['stock_quantity'] == 0 else "white"
        book_frame = tk.Frame(
            parent,
            bg=book_bg_color,
            relief="raised",
            bd=1,
            width=300,
            height=200
        )
        book_frame.pack(side="left", padx=10, fill="both", expand=True)
        book_frame.pack_propagate(False)
        
        # Внутренний контейнер для содержимого карточки
        content_frame = tk.Frame(book_frame, bg=book_bg_color)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Блок с изображением обложки
        cover_frame = tk.Frame(content_frame, bg=book_bg_color)
        cover_frame.pack(side="left", padx=(0, 10))
        
        book_image = self._get_book_image(book['article'])
        if book_image:
            cover_label = tk.Label(cover_frame, image=book_image, bg=book_bg_color)
        else:
            cover_label = tk.Label(
                cover_frame, 
                text="Обложка\nотсутствует", 
                bg=book_bg_color,
                font=("Arial", 8),
                width=12,
                height=8
            )
        cover_label.pack()
        
        # Блок с информацией о книге
        info_frame = tk.Frame(content_frame, bg=book_bg_color)
        info_frame.pack(side="left", fill="both", expand=True)
        
        # Название и автор произведения
        title_font = ("Arial", 10, "bold")
        title_label = tk.Label(
            info_frame,
            text=f"{book['title']} | {book['author']}",
            font=title_font,
            bg=book_bg_color,
            wraplength=180,
            justify="left"
        )
        title_label.pack(anchor="w")
        
        # Жанр произведения
        tk.Label(
            info_frame,
            text=f"Жанр: {book['genre']}",
            font=("Arial", 8),
            bg=book_bg_color,
            justify="left"
        ).pack(anchor="w")
        
        # Информация об издательстве
        tk.Label(
            info_frame,
            text=f"Издательство: {book['publisher']}",
            font=("Arial", 8),
            bg=book_bg_color,
            justify="left"
        ).pack(anchor="w")
        
        # Год издания
        tk.Label(
            info_frame,
            text=f"Год издания: {book['year']}",
            font=("Arial", 8),
            bg=book_bg_color,
            justify="left"
        ).pack(anchor="w")
        
        # Блок с информацией о цене
        price_frame = tk.Frame(info_frame, bg=book_bg_color)
        price_frame.pack(anchor="w")
        
        if book['on_sale'] and book['sale_price']:
            # Отображение акционной цены
            original_price_label = tk.Label(
                price_frame,
                text=f"{book['price']} руб.",
                font=("Arial", 8, "overstrike"),
                fg="red",
                bg=book_bg_color
            )
            original_price_label.pack(side="left")
            
            sale_price_label = tk.Label(
                price_frame,
                text=f" {book['sale_price']} руб.",
                font=("Arial", 9, "bold"),
                fg="black",
                bg=book_bg_color
            )
            sale_price_label.pack(side="left")
        else:
            # Отображение стандартной цены
            tk.Label(
                price_frame,
                text=f"Цена: {book['price']} руб.",
                font=("Arial", 8),
                bg=book_bg_color,
                justify="left"
            ).pack(anchor="w")
        
        # Информация о наличии на складе
        stock_color = "red" if book['stock_quantity'] == 0 else "black"
        tk.Label(
            info_frame,
            text=f"В наличии: {book['stock_quantity']} шт.",
            font=("Arial", 8),
            fg=stock_color,
            bg=book_bg_color,
            justify="left"
        ).pack(anchor="w")
    
    def _on_search_change(self, event):
        """Обработка изменения текста в поле поиска"""
        self._load_books(self.search_entry.get().strip())
    
    def _perform_search(self):
        """Выполнение поиска по введенному запросу"""
        self._load_books(self.search_entry.get().strip())
    
    def run(self):
        """Запуск основного цикла приложения"""
        self.window.mainloop()