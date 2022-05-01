class ImpBook:
    def __init__(self, book, authors, is_borrowed=False):
        self.book = book
        self.authors = authors
        self.is_borrowed = is_borrowed