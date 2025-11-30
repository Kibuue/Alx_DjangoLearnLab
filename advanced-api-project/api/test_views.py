from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Book, Author

class BookAPITests(APITestCase):
    
    def setUp(self):
        # 1. Set up a user for authentication testing
        self.user = User.objects.create_user(username='testuser', password='password')
        
        # 2. Set up initial data
        self.author = Author.objects.create(name="J.K. Rowling")
        self.book = Book.objects.create(
            title="Harry Potter", 
            publication_year=2001, 
            author=self.author
        )
        
        # 3. Define the list URL for convenience
        self.list_url = reverse('book-list')

    def test_list_books(self):
        """Test retrieving the list of books"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_book_authenticated(self):
        """Test that an authenticated user can create a book"""
        self.client.login(username='testuser', password='password')
        data = {
            "title": "New Book",
            "publication_year": 2023,
            "author": self.author.id
        }
        response = self.client.post(reverse('book-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_create_book_unauthenticated(self):
        """Test that unauthenticated users cannot create books"""
        # Ensure we are logged out
        self.client.logout()
        data = {"title": "Hacker Book", "publication_year": 2023, "author": self.author.id}
        response = self.client.post(reverse('book-create'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book(self):
        """Test updating a book"""
        self.client.login(username='testuser', password='password')
        url = reverse('book-update', args=[self.book.id])
        data = {"title": "Harry Potter Updated", "publication_year": 2001, "author": self.author.id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Harry Potter Updated")

    def test_delete_book(self):
        """Test deleting a book"""
        self.client.login(username='testuser', password='password')
        url = reverse('book-delete', args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_filter_books(self):
        """Test filtering books by publication year"""
        # Create a second book with a different year
        Book.objects.create(title="Old Book", publication_year=1990, author=self.author)
        
        # Filter for the original book (2001)
        response = self.client.get(self.list_url, {'publication_year': 2001})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Harry Potter")

    def test_search_books(self):
        """Test searching books by title"""
        Book.objects.create(title="The Hobbit", publication_year=1937, author=self.author)
        
        response = self.client.get(self.list_url, {'search': 'Hobbit'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "The Hobbit")

    def test_ordering_books(self):
        """Test ordering books by publication year"""
        Book.objects.create(title="Old Book", publication_year=1990, author=self.author)
        
        # Order by year descending (newest first)
        response = self.client.get(self.list_url, {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # First book should be Harry Potter (2001), second should be Old Book (1990)
        self.assertEqual(response.data[0]['title'], "Harry Potter")
        self.assertEqual(response.data[1]['title'], "Old Book")