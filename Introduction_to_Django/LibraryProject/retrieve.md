# RETRIEVE
books = Book.objects.all()
print(f"RETRIEVE: Found {books.count()} books")