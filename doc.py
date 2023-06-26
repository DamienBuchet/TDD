import datetime
import unittest

class Book:
    def __init__(self, isbn, title, author, publisher, format, available):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.publisher = publisher
        self.format = format
        self.available = available

    def __str__(self):
        return f"ISBN : {self.isbn}, Titre : {self.title}, Auteur : {self.author}, Éditeur : {self.publisher}, Format : {self.format}, Disponible : {self.available}"


class Member:
    def __init__(self, member_id, code, first_name, last_name, date_of_birth, gender, email):
        self.member_id = member_id
        self.code = code
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.email = email

    def __str__(self):
        return f"ID Membre : {self.member_id}, Code : {self.code}, Prénom : {self.first_name}, Nom : {self.last_name}, Date de naissance : {self.date_of_birth}, Genre : {self.gender}, Email : {self.email}"


class Reservation:
    def __init__(self, reservation_id, member_id, date_limit, book_isbn ):
        self.reservation_id = reservation_id
        self.member_id = member_id
        self.date_limit = date_limit
        self.book_isbn = book_isbn
        self.returned = False
        self.return_date = None

    def return_book(self):
        self.returned = True

    def return_book(self, return_date):
        self.return_date = return_date

    def __str__(self):
        return f"ID de réservation : {self.reservation_id}, ID membre : {self.member_id}, Date limite : {self.date_limit}, ISBN : {self.book_isbn}, Rendu : {self.returned}, Le : {self.return_date}"


class LibraryManagement:
    def __init__(self):
        self.books = []
        self.members = []
        self.reservations = []


class LibraryManagementTests(unittest.TestCase):
    def setUp(self):
        self.library = LibraryManagement()
        self.book1 = Book("1234567890", "Livre 1", "Auteur 1", "Éditeur 1", "Poche", True)
        self.book2 = Book("0987654321", "Livre 2", "Auteur 2", "Éditeur 2", "BD", True)
        self.member = Member(1, "M001", "John", "Doe", datetime.date(1990, 1, 1), "Homme", "damienbuchet@damienbuchet.fr")

    def test_add_book(self):
        self.library.add_book(self.book1)
        self.assertIn(self.book1, self.library.books)

    def test_update_book(self):
        self.library.add_book(self.book1)
        updated_book = Book("1234567890", "Livre 1.2", "Auteur 1.2", "Éditeur 1.2", "Broché", False)
        self.library.update_book(updated_book)
        self.assertEqual(self.book1.title, "Livre 1.2")
        self.assertEqual(self.book1.author, "Auteur 1.2")
        self.assertEqual(self.book1.publisher, "Éditeur 1.2")
        self.assertEqual(self.book1.format, "Broché")
        self.assertFalse(self.book1.available)

    def test_remove_book(self):
        self.library.add_book(self.book1)
        self.library.remove_book(self.book1)
        self.assertNotIn(self.book1, self.library.books)

    def test_search_books_by_title(self):
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)
        result = self.library.search_books_by_title("Livre 1")
        self.assertIn(self.book1, result)
        self.assertNotIn(self.book2, result)

    def test_search_books_by_author(self):
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)
        result = self.library.search_books_by_author("Auteur 1")
        self.assertIn(self.book1, result)
        self.assertNotIn(self.book2, result)

    def test_search_books_by_isbn(self):
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)
        result = self.library.search_books_by_isbn("1234567890")
        self.assertEqual(result, self.book1)
        result = self.library.search_books_by_isbn("0987654321")
        self.assertEqual(result, self.book2)

if __name__ == '__main__':
    unittest.main(exit=False)