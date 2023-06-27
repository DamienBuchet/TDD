import datetime
import unittest
from unittest.mock import MagicMock, patch

from book import Book
from isbnvalidator import ISBNValidator
from librarymanagement import LibraryManagement
from member import Member
from reservation import Reservation
from functions import send_email

class Test(unittest.TestCase):

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

    @patch('mysql.connector.connect')
    def test_execute_select_query_with_mocks(self, mock_connect):
        mock_conn = MagicMock(name='connection')
        mock_connect.return_value = mock_conn
        mock_cursor = MagicMock(name='cursor')
        mock_cursor.fetchall.return_value = [self.book1, self.book2]
        mock_conn.cursor.return_value = mock_cursor

        result = LibraryManagement.get_books()

        mock_connect.assert_called_once()
        mock_cursor.fetchall.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertEqual(result, [self.book1, self.book2])

    @patch('mysql.connector.connect')
    def test_execute_insert_query(self, mock_connect):
        mock_conn = MagicMock(name='connection')
        result = self.library.add_book_bdd(self.book6, mock_conn, mock_connect)
        self.assertEqual(int(result), 1)

    @patch('mysql.connector.connect')
    def test_execute_update_query(self, mock_connect):
        mock_conn = MagicMock(name='connection')
        result = self.library.update_book_bdd(self.book6, mock_conn, mock_connect)
        self.assertEqual(int(result), 1)

    @patch('mysql.connector.connect')
    def test_execute_delete_query(self, mock_connect):
        mock_conn = MagicMock(name='connection')
        result = self.library.del_book_bdd(self.book6, mock_conn, mock_connect)
        self.assertEqual(int(result), True)

    def test_send_email(self):
        reservation1 = Reservation(reservation_id=1, member_id=self.member.member_id, date_limit=datetime.date.today(), book_isbn=self.book1.isbn)
        reservation2 = Reservation(reservation_id=2, member_id=self.member.member_id, date_limit=datetime.date.today(), book_isbn=self.book2.isbn)
        self.library.add_reservation(reservation1)
        self.library.add_reservation(reservation2)
        reservations_to_remind = [reservation for reservation in self.library.reservations if reservation.date_limit < datetime.date.today()]
        members_to_remind = list(set(reservation.member_id for reservation in reservations_to_remind))

        for member_id in members_to_remind:
            member_reservations = [reservation for reservation in reservations_to_remind if reservation.member_id == member_id]
            member_email = LibraryManagement.get_member_email(self, member_id)
            subject = "Rappel : Réservations en retard"
            message = f"Cher membre,\n\nVous avez actuellement les réservations en retard suivantes :\n\n"

            for reservation in member_reservations:
                book_title = LibraryManagement.get_book_title(self, reservation.book_isbn)
                message += f"- Livre : {book_title}, ID de réservation: {reservation.reservation_id}\n"
            smtp_server = MagicMock()

            send_email(smtp_server, "tests_tdd@tdd.test", member_email, subject, message)

            smtp_server.sendmail.assert_called_once_with("tests_tdd@tdd.test", member_email, "Subject: {}\r\n\r\n{}".format(subject, message))
            smtp_server.quit.assert_called_once()

    def test_getCorrectLocator(self):
        self.assertEqual(LibraryManagement.getLocator(self, '9782749941677'), '1677A2')
        self.assertEqual(LibraryManagement.getLocator(self, '9782749906256'), '6256A5')
        self.assertNotEqual(LibraryManagement.getLocator(self, '9782749906256'), '1677A2')

    test_valid_isbn_10 = lambda self: self.assertTrue(ISBNValidator.is_valid_isbn('2749909392'))

    test_invalid_isbn_10 = lambda self: self.assertFalse(ISBNValidator.is_valid_isbn('2749909393'))

    test_letters_isbn_10 = lambda self: self.assertRaises(Exception, ISBNValidator.is_valid_isbn, '27499O9392')

    test_valid_isbn_13 = lambda self: self.assertTrue(ISBNValidator.is_valid_isbn('9782749909394'))

    test_invalid_isbn_13 = lambda self: self.assertFalse(ISBNValidator.is_valid_isbn('9782749909393'))