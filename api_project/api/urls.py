from django.urls import path, include 
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet

# 1. Initialize the router
router = DefaultRouter()

# 2. Register the ViewSet
# The first argument 'books_all' creates the URL prefix
router.register(r'books_all', BookViewSet, basename='book_all')

# 3. Update urlpatterns
urlpatterns = [
    
    path('books/', BookList.as_view(), name='book-list'),

    
    path('', include(router.urls)),
]