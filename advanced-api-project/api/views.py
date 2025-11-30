from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer

# ListView: Retrieve all books
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Allow anyone to read (GET), but restrict write access (though ListAPIView is read-only by default)
    permission_classes = [IsAuthenticatedOrReadOnly]

# DetailView: Retrieve a single book by ID
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# CreateView: Add a new book
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Only authenticated users can create
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # This method is called when saving a new object.
        # It's the perfect place to customize behavior, like adding the current user
        # or performing extra checks before saving.
        # For now, we just save the instance.
        serializer.save()

# UpdateView: Modify an existing book
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Only authenticated users can update
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        # Similar customization hook for updates
        serializer.save()

# DeleteView: Remove a book
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Only authenticated users can delete
    permission_classes = [IsAuthenticated]