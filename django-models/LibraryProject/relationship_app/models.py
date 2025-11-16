from django.db import models


# 1. Author (One author can have many books)
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# 2. Book (Connected to Author via ForeignKey)
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


# 3. Library (Has many books through a ManyToMany relation)
class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name


# 4. Librarian (Each library has exactly one librarian)
class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

