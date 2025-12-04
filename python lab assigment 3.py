# -------------------------------------------------------------
# LIBRARY INVENTORY MANAGER - COMPILED SINGLE FILE (Assignment 3)
# -------------------------------------------------------------

import json
import logging
from pathlib import Path

logging.basicConfig(
    filename="library.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

CATALOG_FILE = Path("catalog.json")


# -------------------------------------------------------------
# TASK 1: BOOK CLASS
# -------------------------------------------------------------
class Book:
    def __init__(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status

    def __str__(self):
        return f"{self.title} | {self.author} | ISBN: {self.isbn} | Status: {self.status}"

    def is_available(self):
        return self.status == "available"

    def issue(self):
        if self.is_available():
            self.status = "issued"
            return True
        return False

    def return_book(self):
        self.status = "available"

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["title"],
            data["author"],
            data["isbn"],
            data["status"]
        )


# -------------------------------------------------------------
# TASK 2–3–5: INVENTORY MANAGER WITH JSON + LOGGING
# -------------------------------------------------------------
class LibraryInventory:
    def __init__(self):
        self.books = []
        self.load_catalog()

    def add_book(self, book):
        self.books.append(book)
        logging.info(f"Book added: {book.title}")
        self.save_catalog()

    def search_by_title(self, title):
        return [b for b in self.books if title.lower() in b.title.lower()]

    def search_by_isbn(self, isbn):
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def display_all(self):
        return self.books

    # JSON SAVE
    def save_catalog(self):
        try:
            data = [b.to_dict() for b in self.books]
            with open(CATALOG_FILE, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            logging.error(f"Error saving catalog: {e}")

    # JSON LOAD
    def load_catalog(self):
        if not CATALOG_FILE.exists():
            logging.warning("Catalog file not found, creating a new one.")
            self.save_catalog()
            return

        try:
            with open(CATALOG_FILE, "r") as f:
                data = json.load(f)
                self.books = [Book.from_dict(d) for d in data]
        except Exception:
            logging.error("Catalog corrupted! Resetting catalog.")
            self.books = []
            self.save_catalog()


# -------------------------------------------------------------
# TASK 4: CLI MENU
# -------------------------------------------------------------
def menu():
    print("\n===== LIBRARY INVENTORY MANAGER =====")
    print("1. Add Book")
    print("2. Issue Book")
    print("3. Return Book")
    print("4. View All Books")
    print("5. Search Book by Title")
    print("6. Exit")


def main():
    inventory = LibraryInventory()

    while True:
        menu()
        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                title = input("Title: ")
                author = input("Author: ")
                isbn = input("ISBN: ")

                book = Book(title, author, isbn)
                inventory.add_book(book)
                print("Book added successfully.")

            elif choice == "2":
                isbn = input("Enter ISBN to issue: ")
                book = inventory.search_by_isbn(isbn)

                if book and book.issue():
                    inventory.save_catalog()
                    print("Book issued successfully.")
                else:
                    print("Book not available or not found.")

            elif choice == "3":
                isbn = input("Enter ISBN to return: ")
                book = inventory.search_by_isbn(isbn)

                if book:
                    book.return_book()
                    inventory.save_catalog()
                    print("Book returned successfully.")
                else:
                    print("Book not found.")

            elif choice == "4":
                print("\n=== ALL BOOKS ===")
                for b in inventory.display_all():
                    print(b)

            elif choice == "5":
                keyword = input("Enter title keyword: ")
                results = inventory.search_by_title(keyword)

                if results:
                    for r in results:
                        print(r)
                else:
                    print("No matching books found.")

            elif choice == "6":
                print("Exiting program...")
                break

            else:
                print("Invalid choice, please try again.")

        except Exception as e:
            print("An error occurred:", e)


# -------------------------------------------------------------
# PROGRAM ENTRY POINT
# -------------------------------------------------------------
if __name__ == "__main__":
    main()
