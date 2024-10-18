import sqlite3
import tkinter as tk
from tkinter import messagebox

# Класс для работы с книгами и базой данных
class BookApp:
    def __init__(self, root):
        self.conn = sqlite3.connect("books.db")
        self.create_table()

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

    # Создание таблицы, если её нет
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                author TEXT,
                genre TEXT,
                year TEXT
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
            cursor.execute('''
                INSERT INTO books (title, author, genre, year)
                VALUES (?, ?, ?, ?)
            ''', (title, author, genre, year))
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
            cursor.execute('''
                SELECT title, author, genre, year FROM books
                WHERE title LIKE ? OR author LIKE ?
            ''', (f'%{search_term}%', f'%{search_term}%'))

            books = cursor.fetchall()

            self.result_text.delete(1.0, tk.END)  # Очистка предыдущих результатов

            if books:
                for book in books:
                    self.result_text.insert(tk.END, f"Title: {book[0]}, Author: {book[1]}, Genre: {book[2]}, Year: {book[3]}\n")
            else:
                self.result_text.insert(tk.END, "No books found.")
        else:
            messagebox.showwarning("Input Error", "Please enter a search term.")

# Запуск приложения
if __name__ == '__main__':
    root = tk.Tk()
    app = BookApp(root)
    root.mainloop()