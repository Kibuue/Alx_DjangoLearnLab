from django.urls import path
from .views import list_books, LibraryDetailView, register_view, login_view, logout_view, admin_view, librarian_view, member_view
from .views import add_book, edit_book, delete_book  # ← Only import the function-based views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # Existing URLs
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('register/', register_view, name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('admin/', admin_view, name='admin_view'),
    path('librarian/', librarian_view, name='librarian_view'),
    path('member/', member_view, name='member_view'),
    
    # Book management URLs with permissions (function-based only)
    path('books/add/', add_book, name='add_book'),
    path('books/<int:pk>/edit/', edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', delete_book, name='delete_book'),
]