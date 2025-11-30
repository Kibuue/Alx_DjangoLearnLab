from django.db import models

class Author(models.Model):
    """
    Represents an author in the system.
    Authors can write multiple books (One-to-Many relationship).
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Book(models.Model):
    """
    Represents a book written by an author.
    Links to the Author model via a ForeignKey.
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    # related_name='books' allows us to access an author's books via author.books.all()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return self.title