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