import json
import os
from datetime import datetime

# Файл для хранения данных
DATA_FILE = "library_data.json"

def load_books():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            print("Ошибка при загрузке файла. Создана новая библиотека.")
            return []
    return []

def save_books(books):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(books, f, ensure_ascii=False, indent=4)
        return True
    except IOError:
        print("Ошибка при сохранении данных!")
        return False

def add_book(books):
    print("\n--- Добавление книги ---")
    title = input("Название: ").strip()
    if not title:
        print("Название не может быть пустым!")
        return
    
    author = input("Автор: ").strip()
    genre = input("Жанр: ").strip()
    
    while True:
        year = input("Год издания: ").strip()
        if year.isdigit():
            break
        print("Год должен быть числом!")
    
    description = input("Краткое описание: ").strip()
    
    book = {
        "id": len(books) + 1,
        "title": title,
        "author": author,
        "genre": genre,
        "year": int(year),
        "description": description,
        "status": "не прочитана",
        "favorite": False,
        "added_date": datetime.now().strftime("%Y-%m-%d")
    }
    
    books.append(book)
    if save_books(books):
        print(f"Книга '{title}' успешно добавлена!")
    else:
        print("Книга добавлена, но не сохранена в файл.")

def view_books(books):
    if not books:
        print("\nБиблиотека пуста.")
        return

    print("\n--- Просмотр книг ---")
    print("1. Все книги")
    print("2. Сортировать по названию")
    print("3. Сортировать по автору")
    print("4. Сортировать по году")
    print("5. Фильтр по жанру")
    print("6. Фильтр по статусу")
    print("7. Только избранные")
    
    choice = input("Выберите опцию (1-7): ").strip()
    filtered_books = books[:]
    
    if choice == "2":
        filtered_books.sort(key=lambda x: x["title"].lower())
    elif choice == "3":
        filtered_books.sort(key=lambda x: x["author"].lower())
    elif choice == "4":
        filtered_books.sort(key=lambda x: x["year"])
    elif choice == "5":
        genre = input("Введите жанр для фильтрации: ").strip()
        filtered_books = [b for b in books if b["genre"].lower() == genre.lower()]
    elif choice == "6":
        print("1. Прочитана | 2. Не прочитана")
        status_choice = input("Выберите статус: ").strip()
        status = "прочитана" if status_choice == "1" else "не прочитана"
        filtered_books = [b for b in books if b["status"] == status]
    elif choice == "7":
        filtered_books = [b for b in books if b["favorite"]]
    
    if not filtered_books:
        print("Нет книг для отображения.")
        return

    print(f"\n{'ID':<5} {'Название':<30} {'Автор':<20} {'Год':<6} {'Статус':<12} {'Избранное':<10}")
    print("-" * 90)
    for book in filtered_books:
        fav = "Да" if book["favorite"] else "Нет"
        print(f"{book['id']:<5} {book['title']:<30} {book['author']:<20} {book['year']:<6} {book['status']:<12} {fav:<10}")

def toggle_favorite(books):
    view_books(books)
    if not books:
        return
        
    book_id = input("\nВведите ID книги для изменения избранного: ").strip()
    book = find_book_by_id(books, book_id)
    
    if book:
        book["favorite"] = not book["favorite"]
        status = "добавлена в" if book["favorite"] else "удалена из"
        print(f"Книга '{book['title']}' {status} избранное.")
        save_books(books)
    else:
        print("Книга не найдена.")

def change_status(books):
    view_books(books)
    if not books:
        return

    book_id = input("\nВведите ID книги для изменения статуса: ").strip()
    book = find_book_by_id(books, book_id)
    
    if book:
        print(f"Текущий статус: {book['status']}")
        print("1. Прочитана | 2. Не прочитана")
        choice = input("Выберите новый статус: ").strip()
        
        if choice == "1":
            book["status"] = "прочитана"
        elif choice == "2":
            book["status"] = "не прочитана"
        else:
            print("Неверный выбор.")
            return
            
        print(f"Статус книги '{book['title']}' изменен на '{book['status']}'.")
        save_books(books)
    else:
        print("Книга не найдена.")

def delete_book(books):
    view_books(books)
    if not books:
        return

    book_id = input("\nВведите ID книги для удаления: ").strip()
    book = find_book_by_id(books, book_id)
    
    if book:
        confirm = input(f"Вы уверены, что хотите удалить '{book['title']}'? (да/нет): ").strip().lower()
        if confirm == "да":
            books.remove(book)
            for i, b in enumerate(books):
                b["id"] = i + 1
            if save_books(books):
                print("Книга успешно удалена.")
        else:
            print("Удаление отменено.")
    else:
        print("Книга не найдена.")

def search_books(books):
    print("\n--- Поиск книг ---")
    keyword = input("Введите ключевое слово: ").strip().lower()
    
    if not keyword:
        print("Поисковый запрос не может быть пустым.")
        return
    
    results = [
        b for b in books 
        if keyword in b["title"].lower() or 
           keyword in b["author"].lower() or 
           keyword in b["description"].lower()
    ]
    
    if results:
        print(f"\nНайдено {len(results)} книг(и):")
        print(f"{'ID':<5} {'Название':<30} {'Автор':<20} {'Год':<6}")
        print("-" * 65)
        for book in results:
            print(f"{book['id']:<5} {book['title']:<30} {book['author']:<20} {book['year']:<6}")
    else:
        print("Книги по вашему запросу не найдены.")

def find_book_by_id(books, book_id):
    try:
        bid = int(book_id)
        for book in books:
            if book["id"] == bid:
                return book
    except ValueError:
        pass
    return None

def show_favorites(books):
    favorites = [b for b in books if b["favorite"]]
    if favorites:
        print("\n--- Избранные книги ---")
        print(f"{'ID':<5} {'Название':<30} {'Автор':<20} {'Год':<6} {'Статус':<12}")
        print("-" * 80)
        for book in favorites:
            print(f"{book['id']:<5} {book['title']:<30} {book['author']:<20} {book['year']:<6} {book['status']:<12}")
    else:
        print("\nУ вас нет избранных книг.")

def show_menu():
    print("\n" + "=" * 50)
    print("           T-БИБЛИОТЕКА")
    print("=" * 50)
    print("1. Добавить книгу")
    print("2. Просмотреть книги")
    print("3. Избранное (список)")
    print("4. Добавить/Удалить из избранного")
    print("5. Изменить статус книги")
    print("6. Удалить книгу")
    print("7. Поиск книги")
    print("8. Выход")
    print("=" * 50)

def main():
    print("Добро пожаловать в T-Библиотеку!")
    books = load_books()
    print(f"Загружено {len(books)} книг(и).")
    
    while True:
        show_menu()
        choice = input("Выберите действие (1-8): ").strip()
        
        if choice == "1":
            add_book(books)
        elif choice == "2":
            view_books(books)
        elif choice == "3":
            show_favorites(books)
        elif choice == "4":
            toggle_favorite(books)
        elif choice == "5":
            change_status(books)
        elif choice == "6":
            delete_book(books)
        elif choice == "7":
            search_books(books)
        elif choice == "8":
            save_books(books)
            print("\nСпасибо за использование T-Библиотеки. До свидания!")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()