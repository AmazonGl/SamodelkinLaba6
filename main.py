import sqlite3
import tkinter as tk
from tkinter import messagebox

# Класс для работы с книгами и базой данных
class BookApp:
    def __init__(self, root):
        self.conn = sqlite3.connect("books.db")
        self.create_tables()

        self.root = root
        self.root.title("Book Library")

        # Поля ввода для добавления книги
        self.label_title = tk.Label(root, text="Title:")
        self.label_title.grid(row=0, column=0)
        self.entry_title = tk.Entry(root)
        self.entry_title.grid(row=0, column=1)

        self.label_author = tk.Label(root, text="Author:")
        self.label_author.grid(row=1, column=0)
        self.entry_author = tk.Entry(root)
        self.entry_author.grid(row=1, column=1)

        self.label_genre = tk.Label(root, text="Genre:")
        self.label_genre.grid(row=2, column=0)
        self.entry_genre = tk.Entry(root)
        self.entry_genre.grid(row=2, column=1)

        self.label_year = tk.Label(root, text="Year:")
        self.label_year.grid(row=3, column=0)
        self.entry_year = tk.Entry(root)
        self.entry_year.grid(row=3, column=1)

        # Кнопка для добавления книги
        self.add_button = tk.Button(root, text="Add Book", command=self.add_book)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Поля ввода для поиска книги
        self.label_search = tk.Label(root, text="Search by Title or Author:")
        self.label_search.grid(row=5, column=0)
        self.entry_search = tk.Entry(root)
        self.entry_search.grid(row=5, column=1)

        # Кнопка для поиска книги
        self.search_button = tk.Button(root, text="Search", command=self.search_books)
        self.search_button.grid(row=6, column=0, columnspan=2, pady=10)

        # Поле для отображения результатов поиска
        self.result_text = tk.Text(root, height=10, width=50)
        self.result_text.grid(row=7, column=0, columnspan=2)

    # Создание таблиц в базе данных
    def create_tables(self):
        cursor = self.conn.cursor()

        # Таблица авторов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS authors (
                author_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')

        # Таблица жанров
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS genres (
                genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
                genre_name TEXT NOT NULL
            )
        ''')

        # Таблица книг
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                year TEXT NOT NULL,
                author_id INTEGER,
                genre_id INTEGER,
                FOREIGN KEY (author_id) REFERENCES authors(author_id),
                FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
            )
        ''')

        self.conn.commit()

    # Метод для добавления книги в БД
    def add_book(self):
        title = self.entry_title.get()
        author = self.entry_author.get()
        genre = self.entry_genre.get()
        year = self.entry_year.get()

        if title and author and genre and year:
            cursor = self.conn.cursor()

            # Проверяем, есть ли уже такой автор, если нет — добавляем
            cursor.execute("SELECT author_id FROM authors WHERE name = ?", (author,))
            author_id = cursor.fetchone()
            if author_id is None:
                cursor.execute("INSERT INTO authors (name) VALUES (?)", (author,))
                author_id = cursor.lastrowid
            else:
                author_id = author_id[0]

            # Проверяем, есть ли уже такой жанр, если нет — добавляем
            cursor.execute("SELECT genre_id FROM genres WHERE genre_name = ?", (genre,))
            genre_id = cursor.fetchone()
            if genre_id is None:
                cursor.execute("INSERT INTO genres (genre_name) VALUES (?)", (genre,))
                genre_id = cursor.lastrowid
            else:
                genre_id = genre_id[0]

            # Добавляем книгу с author_id и genre_id
            cursor.execute('''
                INSERT INTO books (title, year, author_id, genre_id)
                VALUES (?, ?, ?, ?)
            ''', (title, year, author_id, genre_id))

            self.conn.commit()
            messagebox.showinfo("Success", f"Book '{title}' added successfully!")
            self.clear_entries()
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    # Очистка полей ввода
    def clear_entries(self):
        self.entry_title.delete(0, tk.END)
        self.entry_author.delete(0, tk.END)
        self.entry_genre.delete(0, tk.END)
        self.entry_year.delete(0, tk.END)

    # Метод для поиска книг в БД
    def search_books(self):
        search_term = self.entry_search.get()

        if search_term:
            cursor = self.conn.cursor()
            # Запрос с объединением таблиц
            cursor.execute('''
                SELECT books.title, books.year, authors.name, genres.genre_name 
                FROM books
                JOIN authors ON books.author_id = authors.author_id
                JOIN genres ON books.genre_id = genres.genre_id
                WHERE books.title LIKE ? OR authors.name LIKE ?
            ''', (f'%{search_term}%', f'%{search_term}%'))

            books = cursor.fetchall()

            self.result_text.delete(1.0, tk.END)  # Очистка предыдущих результатов

            if books:
                for book in books:
                    # Вывод данных в столбик
                    self.result_text.insert(tk.END, f"Title: {book[0]}\n")
                    self.result_text.insert(tk.END, f"Year: {book[1]}\n")
                    self.result_text.insert(tk.END, f"Author: {book[2]}\n")
                    self.result_text.insert(tk.END, f"Genre: {book[3]}\n")
                    self.result_text.insert(tk.END, "-" * 40 + "\n")  # Разделитель между записями
            else:
                self.result_text.insert(tk.END, "No books found.\n")
        else:
            messagebox.showwarning("Input Error", "Please enter a search term.")

# Запуск приложения
if __name__ == '__main__':
    root = tk.Tk()
    app = BookApp(root)
    root.mainloop()