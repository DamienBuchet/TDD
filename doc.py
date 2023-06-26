# Modules compris dans l'installation de base de Python
import base64
import datetime
import json
import os
import random
import smtplib
import unittest
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# Modules complémentaires
# pip install mysql-connector
import mysql.connector
import requests
# pip install python-dotenv
from dotenv import load_dotenv

load_dotenv()

DB_HOST=base64.b64decode(os.environ.get("DB_HOST")).decode()
DB_USER=base64.b64decode(os.environ.get("DB_USER")).decode()
DB_PASSWORD=base64.b64decode(os.environ.get("DB_PASSWORD")).decode()
DB_NAME=base64.b64decode(os.environ.get("DB_NAME")).decode()
SMTP_HOST=base64.b64decode(os.environ.get("SMTP_HOST")).decode()
SMTP_USER=base64.b64decode(os.environ.get("SMTP_USER")).decode()
SMTP_PASSWORD=base64.b64decode(os.environ.get("SMTP_PASSWORD")).decode()

mydb = mysql.connector.connect(
          host=DB_HOST,
          user=DB_USER,
          password=DB_PASSWORD,
          database=DB_NAME
        )

mycursor = mydb.cursor()

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

    def send_reminder_emails(self):
        reservations_to_remind = [reservation for reservation in self.reservations if reservation.date_limit < datetime.date.today()]
        members_to_remind = list(set(reservation.member_id for reservation in reservations_to_remind))

        for member_id in members_to_remind:
            member_reservations = [reservation for reservation in reservations_to_remind if reservation.member_id == member_id]
            member_email = LibraryManagement.get_member_email(self, member_id)
            subject = "Rappel : Réservations en retard"
            message = f"Cher membre,\n\nVous avez actuellement les réservations en retard suivantes :\n\n"

            for reservation in member_reservations:
                book_title = LibraryManagement.get_book_title(self, reservation.book_isbn)
                message += f"- Livre : {book_title}, ID de réservation: {reservation.reservation_id}\n"
            try:
                send_mail(member_email, subject, message)
                return True
            except:
                return False

def send_mail(recipient, subject, message):
    smtp_host = SMTP_HOST
    smtp_port = 587 
    smtp_username = SMTP_USER
    smtp_password = SMTP_PASSWORD
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = recipient
    msg['Subject'] = subject
    body = MIMEText(message)
    msg.attach(body)
    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.timeout = 2
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
        return True
    except smtplib.SMTPException as e:
        raise Exception

class ISBNValidator:

    def is_valid_isbn(isbn):
        contains_letter = ''
        contains_letter = any(char.isalpha() for char in isbn.lower()) if isbn[-1] != 'X' else False
        if contains_letter:
            raise Exception
        else:
            return Exception if contains_letter else ISBNValidator._is_valid_10_digit_isbn(isbn) if len(isbn) == 10 else ISBNValidator._is_valid_13_digit_isbn(isbn) if len(isbn) == 13 else False
    
    _is_valid_10_digit_isbn = lambda isbn: (sum(int(isbn[i]) * (10 - i) for i in range(len(isbn) - 1)) + (10 if isbn[-1] == 'X' else int(isbn[-1]))) % 11 == 0
    
    _is_valid_13_digit_isbn = lambda isbn: sum(int(isbn[i]) if i % 2 == 0 else int(isbn[i]) * 3 for i in range(len(isbn))) % 10 == 0

class ISBNValidatorTest(unittest.TestCase):

    test_valid_isbn_10 = lambda self: self.assertTrue(ISBNValidator.is_valid_isbn('2749909392'))

    test_invalid_isbn_10 = lambda self: self.assertFalse(ISBNValidator.is_valid_isbn('2749909393'))

    test_letters_isbn_10 = lambda self: self.assertRaises(Exception, ISBNValidator.is_valid_isbn, '27499O9392')

    test_valid_isbn_13 = lambda self: self.assertTrue(ISBNValidator.is_valid_isbn('9782749909394'))

    test_invalid_isbn_13 = lambda self: self.assertFalse(ISBNValidator.is_valid_isbn('9782749909393'))

class BookNotFoundException(Exception):
    pass


class InvalidISBNException(Exception):
    pass

class LibraryManagementTests(unittest.TestCase):
    def setUp(self):
        self.library = LibraryManagement()
        self.book1 = Book("9782749906256", "Le Feu dans le Ciel", "Anne Robillard", "Michel Lafon", "Poche", True)
        self.book2 = Book("9782749906621", "Les Dragons de l'Empereur Noir", "Anne Robillard", "Michel Lafon", "Poche", True)
        self.book3 = Book("9782749907475", "Piège au Royaume des Ombres", "Anne Robillard", "Michel Lafon", "Poche", True)
        self.book4 = Book("9782749907833", "La Princesse rebelle", "Anne Robillard", "Michel Lafon", "Poche", True)
        self.book5 = Book("9782749908724", "L'Île des lézards", "Anne Robillard", "Michel Lafon", "Poche", True)
        self.book6 = Book("9782749909394", "Le Journal d'Onyx", "Anne Robillard", "Michel Lafon", "Poche", True)
        self.book7 = Book("9782749909691", "L'enlèvement", "Anne Robillard", "Michel Lafon", "Poche", True)
        self.book8 = Book("9782749910147", "Les Dieux déchus", "Anne Robillard", "Michel Lafon", "Poche", True)
        self.book9 = Book("9782749911052", "L'héritage de Danalieth", "Anne Robillard", "Michel Lafon", "Poche", True)
        self.book10 = Book("9782749911540", "Représailles", "Anne Robillard", "Michel Lafon", "Poche", True)
        self.book11 = Book("9782749911939", "La Justice céleste", "Anne Robillard", "Michel Lafon", "Poche", True)
        self.book12 = Book("9782749911946", "Irianeth", "Anne Robillard", "Michel Lafon", "Poche", True)
        self.book13 = Book("2857045603", "L'apprenti assassin", "Robin Hobb", "Pygmalion Editions", "Poche", True)
        self.member = Member(1, "M001", "John", "Doe", datetime.date(1990, 1, 1), "Homme", "damienbuchet@damienbuchet.fr")

    def test_add_book(self):
        self.library.add_book(self.book1)
        self.assertIn(self.book1, self.library.books)

    def test_update_book(self):
        self.library.add_book(self.book1)
        updated_book = Book("9782749906256", "Livre 1.2", "Auteur 1.2", "Éditeur 1.2", "Broché", False)
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
        result = self.library.search_books_by_title("Le Feu dans le Ciel")
        self.assertIn(self.book1, result)
        self.assertNotIn(self.book2, result)

    def test_search_books_by_author(self):
        self.library.add_book(self.book1)
        self.library.add_book(self.book13)
        result = self.library.search_books_by_author("Anne Robillard")
        self.assertIn(self.book1, result)
        self.assertNotIn(self.book2, result)

    def test_search_books_by_isbn(self):
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)
        result = self.library.search_books_by_isbn("9782749906256")
        self.assertEqual(result, self.book1)
        result = self.library.search_books_by_isbn("9782749906621")
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

    def test_add_reservation(self):
        reservation = Reservation(reservation_id=1, member_id=self.member.member_id, date_limit=datetime.date.today(), book_isbn=self.book1.isbn)
        self.library.add_reservation(reservation)
        self.assertIn(reservation, self.library.reservations)

    def test_update_reservation(self):
        reservation = Reservation(reservation_id=1, member_id=self.member.member_id, date_limit=datetime.date.today(), book_isbn=self.book1.isbn)
        self.library.add_reservation(reservation)
        updated_reservation = Reservation(reservation_id=1, member_id=self.member.member_id, date_limit=datetime.date.today() + datetime.timedelta(days=7), book_isbn=self.book1.isbn)
        self.library.update_reservation(updated_reservation)
        self.assertEqual(reservation.return_date, updated_reservation.return_date)

    def test_remove_reservation(self):
        reservation = Reservation(reservation_id=1, member_id=self.member.member_id, date_limit=datetime.date.today(), book_isbn=self.book1.isbn)
        self.library.add_reservation(reservation)
        self.library.remove_reservation(reservation)
        self.assertNotIn(reservation, self.library.reservations)

    def test_make_reservation(self):
        self.library.add_member(self.member)
        self.library.add_book(self.book1)
        reservation = self.library.make_reservation(self.member, self.book1)
        self.assertIn(reservation, self.library.reservations)

    def test_cancel_reservation(self):
        reservation = Reservation(reservation_id=1, member_id=self.member.member_id, date_limit=datetime.date.today(), book_isbn=self.book1.isbn)
        self.library.add_reservation(reservation)
        self.library.cancel_reservation(reservation)
        self.assertNotIn(reservation, self.library.reservations)

    def test_get_open_reservations(self):
        self.library.add_member(self.member)
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)
        reservation1 = self.library.make_reservation(self.member, self.book1)
        reservation2 = self.library.make_reservation(self.member, self.book2)
        reservations = self.library.get_open_reservations(self.member)
        self.assertIn(reservation1, reservations)
        self.assertIn(reservation2, reservations)

    def test_get_reservation_history(self):
        reservation1 = Reservation(reservation_id=1, member_id=self.member.member_id, date_limit=datetime.date.today(), book_isbn=self.book1.isbn)
        reservation2 = Reservation(reservation_id=2, member_id=self.member.member_id, date_limit=datetime.date.today(), book_isbn=self.book2.isbn)
        self.library.add_reservation(reservation1)
        self.library.add_reservation(reservation2)
        reservation2.return_book(datetime.date.today())
        history = self.library.get_reservation_history(self.member)
        self.assertEqual(len(history), 2)
        self.assertIn(reservation1, history)
        self.assertIn(reservation2, history)

    def test_add_book_in_bdd(self):
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)
        sql = f"SELECT COUNT(*) as res FROM books"
        mycursor.execute(sql)
        res = mycursor.fetchall()[0][0]
        nb_livres_bdd = int(res)
        nb_livres = 0
        for book in self.library.books:
            nb_livres += 1
            sql = f"INSERT INTO `books`(`isbn`, `title`, `author`, `publisher`, `format`, `available`) VALUES ('{book.isbn}',\"{book.title}\",'{book.author}','{book.publisher}','{book.format}','{book.available}')"
            mycursor.execute(sql)
            mydb.commit()
        sql = f"SELECT COUNT(*) as res FROM books"
        mycursor.execute(sql)
        res = mycursor.fetchall()[0][0]
        ins_livres = res
        self.assertEqual(nb_livres_bdd + nb_livres, ins_livres)

    def test_add_member_in_bdd(self):
        self.library.add_member(self.member)
        sql = f"SELECT COUNT(*) as res FROM members"
        mycursor.execute(sql)
        res = mycursor.fetchall()[0][0]
        nb_membres_bdd = int(res)
        nb_membres = 0
        for member in self.library.members:
            nb_membres += 1
            sql = f"INSERT INTO `members`(`member_id`, `code`, `firstname`, `lastname`, `birthdate`, `gender`, `email`) VALUES ('{member.member_id}','{member.code}','{member.first_name}','{member.last_name}','{member.date_of_birth}','{member.gender}','{member.email}')"
            mycursor.execute(sql)
            mydb.commit()
        sql = f"SELECT COUNT(*) as res FROM members"
        mycursor.execute(sql)
        res = mycursor.fetchall()[0][0]
        ins_membres = res
        self.assertEqual(nb_membres_bdd + nb_membres, ins_membres)

    def test_send_reminder_emails(self):
        self.library.add_member(self.member)
        self.library.add_book(self.book1)
        past_date = datetime.date.today() - datetime.timedelta(days=7)
        self.reservation1 = Reservation(1, self.member.member_id, past_date, self.book1.isbn)
        self.reservation2 = Reservation(2, self.member.member_id, past_date, self.book2.isbn)
        self.library.reservations = [self.reservation1, self.reservation2]
        self.assertTrue(self.library.send_reminder_emails())

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

    def test_getCorrectLocator(self):
        self.assertEqual(self.getLocator('9782749941677'), '1677A2')
        self.assertEqual(self.getLocator('9782749906256'), '6256A5')
        self.assertNotEqual(self.getLocator('9782749906256'), '1677A2')

if __name__ == '__main__':
    unittest.main(exit=False)