import datetime
import requests
import json
import random
from book import Book
from isbnvalidator import ISBNValidator
from booknotfound import BookNotFoundException
from invalidisbn import InvalidISBNException
from reservation import Reservation
from mysqlclass import MySQLClass

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

    def execute_select_query(query):
        my_obj = MySQLClass()
        result = my_obj.execute_select_query(query)
        return result
    
    def get_books():
        query = 'SELECT * FROM books'
        result = LibraryManagement.execute_select_query(query)
        return result

    def add_book_bdd(self, book, conn, connect):
        connect.return_value = conn
        result = conn.execute_other_query(f"INSERT INTO `books`(`isbn`, `title`, `author`, `publisher`, `format`, `available`) VALUES ('{book.isbn}','{book.title}','{book.author}','{book.publisher}','{book.format}','{book.available}')")
        return result

    def update_book_bdd(self, book, conn, connect):
        connect.return_value = conn
        result = conn.execute_other_query(f"UPDATE `books` SET `title` = 'Titre modifié' WHERE `isbn` = {book.isbn}")
        return result
    
    def del_book_bdd(self, book, conn, connect):
        connect.return_value = conn
        result = conn.execute_other_query(f"DELETE FROM `books` WHERE `isbn` = {book.isbn}")
        return result
    
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

    def search_member_by_id(self, member_id):
        for member in self.members:
            if member.member_id == member_id:
                return member
        return None

    def get_member_email(self, member_id):
        member = self.search_member_by_id(member_id)
        if member:
            return member.email
        return None

    def add_reservation(self, reservation):
        self.reservations.append(reservation)

    def update_reservation(self, reservation):
        for i in range(len(self.reservations)):
            if self.reservations[i].reservation_id == reservation.reservation_id:
                self.reservations[i] = reservation
                break

    def remove_reservation(self, reservation):
        self.reservations.remove(reservation)

    def make_reservation(self, member, book):
        if len(self.get_open_reservations(member)) >= 3:
            raise Exception("Le nombre maximum de réservations a été atteint pour ce membre")
        date_limit = datetime.date.today() + datetime.timedelta(days=120)
        reservation_id = len(self.reservations) + 1
        reservation = Reservation(reservation_id, member.member_id, date_limit, book.isbn)
        self.reservations.append(reservation)
        return reservation

    def cancel_reservation(self, reservation):
        self.reservations.remove(reservation)

    def get_open_reservations(self, member=None):
        if member:
            return [reservation for reservation in self.reservations if reservation.member_id == member.member_id]
        else:
            return self.reservations

    def get_reservation_history(self, member):
        return [reservation for reservation in self.reservations if reservation.member_id == member.member_id]
    
    def getLocator(self, isbn):
        self.library.add_book(self.book1)
        book = self.library.search_books_by_isbn(isbn)
        if book is not None:
            locator = str(str(book.isbn)[-4:]) + str((book.author)[0]) + str(len((book.title).split()))
            return locator
        else:
            try:
                r = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}")
                x = json.loads(json.dumps(r.json(), indent=4))
                y = json.loads(json.dumps(x['items'], indent=4))
                try:
                    publisher = y[0]['volumeInfo']['publisher']
                except:
                    publisher = "Éditeur inconnu"
                book = Book(isbn, y[0]['volumeInfo']['title'], y[0]['volumeInfo']['authors'][0], publisher, random.choice(["Poche", "Broché", "BD"]), random.choice([True, False]))
                locator = str(str(book.isbn)[-4:]) + str((book.author)[0]) + str(len((book.title).split()))
                return locator
            except:
                test_valid = ISBNValidator.is_valid_isbn(isbn)
                if test_valid:
                    raise BookNotFoundException
                else:
                    raise InvalidISBNException