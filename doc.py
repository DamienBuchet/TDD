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

    def add_book(self, book):
        self.books.append(book)

    def update_book(self, book):
        for i, b in enumerate(self.books):
            if b.isbn == book.isbn:
                self.books[i].title = book.title
                self.books[i].author = book.author
                self.books[i].publisher = book.publisher
                self.books[i].format = book.format
                self.books[i].available = book.available
                break

    def remove_book(self, book):
        self.books.remove(book)

    def search_books_by_title(self, title):
        result = []
        for book in self.books:
            if book.title.lower() == title.lower():
                result.append(book)
        return result

    def search_books_by_author(self, author):
        result = []
        for book in self.books:
            if book.author.lower() == author.lower():
                result.append(book)
        return result

    def search_books_by_isbn(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def get_book_title(self, isbn):
        book = self.search_books_by_isbn(isbn)
        if book:
            return book.title
        return None
    
    def add_member(self, member):
        self.members.append(member)

    def update_member(self, member):
        for i in range(len(self.members)):
            if self.members[i].member_id == member.member_id:
                self.members[i].first_name = member.first_name
                self.members[i].last_name = member.last_name
                self.members[i].date_of_birth = member.date_of_birth
                self.members[i].gender = member.gender
                self.members[i].email = member.email
                break

    def remove_member(self, member):
        self.members.remove(member)

    def search_members_by_name(self, name):
        result = []
        for member in self.members:
            if name.lower() in (member.first_name.lower() + " " + member.last_name.lower()):
                result.append(member)
        return result

    def search_member_by_code(self, code):
        for member in self.members:
            if member.code == code:
                return member
        return None

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

    def test_add_member(self):
        self.library.add_member(self.member)
        self.assertIn(self.member, self.library.members)

    def test_update_member(self):
        self.library.add_member(self.member)
        updated_member = Member(1, "M001", "John", "Doe", datetime.date(1990, 1, 1), "Femme", "damienbuchetdb@gmail.com")
        self.library.update_member(updated_member)
        self.assertEqual(self.member.gender, "Femme")
        self.assertEqual(self.member.email, "damienbuchetdb@gmail.com")

    def test_remove_member(self):
        self.library.add_member(self.member)
        self.library.remove_member(self.member)
        self.assertNotIn(self.member, self.library.members)

    def test_search_members_by_name(self):
        self.library.add_member(self.member)
        result = self.library.search_members_by_name("John Doe")
        self.assertEqual(result, [self.member])

    def test_search_member_by_code(self):
        self.library.add_member(self.member)
        result = self.library.search_member_by_code("M001")
        self.assertEqual(result, self.member)

    def test_get_member_email(self):
        self.library.add_member(self.member)
        email = self.library.get_member_email(self.member.member_id)
        self.assertEqual(email, "damienbuchet@damienbuchet.fr")

if __name__ == '__main__':
    unittest.main(exit=False)