from bookshelf.models import Book

# CREATE
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(book)

# RETRIEVE
books = Book.objects.all()
print(books)

# UPDATE
book.title = "Nineteen Eighty-Four"
book.save()
print(book.title)

# DELETE
book.delete()
