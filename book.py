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