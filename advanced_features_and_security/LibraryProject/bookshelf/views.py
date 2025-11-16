"""
Secure views implementing best practices:
- Uses Django ORM (prevents SQL injection)
- Validates all user input
- Implements CSRF protection
- Proper permission checks
- Error handling
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from .models import Book
from .forms import BookForm
from .forms import ExampleForm

# =====================================================
# SECURE BOOK VIEWS
# =====================================================

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    Display list of books with secure search functionality.
    
    Security features:
    - Uses Django ORM (prevents SQL injection)
    - Input validation through Django's query methods
    - Permission check
    """
    books = Book.objects.all()
    
    # Secure search implementation
    search_query = request.GET.get('search', '').strip()
    if search_query:
        # Using Django ORM's Q objects - automatically parameterized
        # This prevents SQL injection
        books = books.filter(
            Q(title__icontains=search_query) | 
            Q(author__icontains=search_query)
        )
        
        # Limit search results to prevent DoS
        books = books[:100]
    
    return render(request, 'bookshelf/book_list.html', {
        'books': books,
        'search_query': search_query
    })


@permission_required('bookshelf.can_create', raise_exception=True)
@require_http_methods(["GET", "POST"])  # Only allow GET and POST
@csrf_protect  # Explicit CSRF protection (already in middleware)
def book_create(request):
    """
    Create a new book using secure form handling.
    
    Security features:
    - Uses Django ModelForm (automatic validation)
    - CSRF protection via {% csrf_token %}
    - Input sanitization in form clean methods
    - Permission check
    """
    if request.method == 'POST':
        # Use Django form for automatic validation and sanitization
        form = BookForm(request.POST)
        
        if form.is_valid():
            # form.save() uses Django ORM - prevents SQL injection
            book = form.save()
            messages.success(request, f'Book "{book.title}" created successfully!')
            return redirect('book_list')
        else:
            # Display form validation errors
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookForm()
    
    return render(request, 'bookshelf/book_form.html', {
        'form': form,
        'action': 'Create'
    })


@permission_required('bookshelf.can_edit', raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def book_edit(request, pk):
    """
    Edit an existing book securely.
    
    Security features:
    - Uses get_object_or_404 (prevents information disclosure)
    - Django ModelForm for validation
    - CSRF protection
    - Permission check
    """
    # get_object_or_404 prevents timing attacks
    # Returns 404 instead of revealing if object exists
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" updated successfully!')
            return redirect('book_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'bookshelf/book_form.html', {
        'form': form,
        'book': book,
        'action': 'Edit'
    })


@permission_required('bookshelf.can_delete', raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def book_delete(request, pk):
    """
    Delete a book with confirmation.
    
    Security features:
    - Requires POST for deletion (prevents CSRF via GET)
    - Confirmation page
    - Permission check
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f'Book "{title}" deleted successfully!')
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_confirm_delete.html', {
        'book': book
    })


# =====================================================
# EXAMPLE: INSECURE vs SECURE CODE
# =====================================================

def insecure_search_example(request):
    """
    ❌ INSECURE EXAMPLE - DO NOT USE!
    
    This demonstrates what NOT to do:
    - Raw SQL with string formatting (SQL injection vulnerability)
    - No input validation
    - No CSRF protection
    """
    search = request.GET.get('q', '')
    
    # ❌ VULNERABLE TO SQL INJECTION!
    # query = f"SELECT * FROM bookshelf_book WHERE title LIKE '%{search}%'"
    # results = Book.objects.raw(query)
    
    # An attacker could input: ' OR '1'='1
    # Resulting query: SELECT * FROM bookshelf_book WHERE title LIKE '%' OR '1'='1%'
    # This would return ALL books!
    
    return render(request, 'bookshelf/search.html', {'results': []})


def secure_search_example(request):
    """
    ✅ SECURE EXAMPLE - USE THIS!
    
    Security features:
    - Uses Django ORM (parameterized queries)
    - Input validation
    - Limited results
    """
    search = request.GET.get('q', '').strip()
    
    # Validate input
    if len(search) > 100:
        messages.error(request, 'Search query too long.')
        return redirect('book_list')
    
    # ✅ SECURE: Django ORM automatically parameterizes this query
    results = Book.objects.filter(title__icontains=search)[:50]
    
    return render(request, 'bookshelf/search.html', {'results': results})


# =====================================================
# EXAMPLE FORM VIEW
# =====================================================

@login_required
@csrf_protect
def form_example(request):
    """
    Example view demonstrating secure form handling.
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        
        if form.is_valid():
            # Process the validated and sanitized data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Do something with the data (save to DB, send email, etc.)
            messages.success(request, 'Form submitted successfully!')
            return redirect('form_example')
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/form_example.html', {'form': form})