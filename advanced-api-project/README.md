## Advanced API Project: Views and Permissions

This project utilizes Django REST Framework's Generic Views to handle CRUD operations for the Book model.

### View Configuration (`api/views.py`)

* **ListView (`/books/`):**
    * **Type:** `generics.ListAPIView`
    * **Permission:** `IsAuthenticatedOrReadOnly`
    * **Behavior:** Returns a list of all books. Unauthenticated users can access this view (ReadOnly).

* **DetailView (`/books/<int:pk>/`):**
    * **Type:** `generics.RetrieveAPIView`
    * **Permission:** `IsAuthenticatedOrReadOnly`
    * **Behavior:** Returns the details of a specific book by ID. Unauthenticated users can view.

* **CreateView (`/books/create/`):**
    * **Type:** `generics.CreateAPIView`
    * **Permission:** `IsAuthenticated` (Strict)
    * **Behavior:** Allows authenticated users to add a new book.
    * **Custom Hooks:** Includes `perform_create` to handle custom logic during object creation.

* **UpdateView (`/books/update/<int:pk>/`):**
    * **Type:** `generics.UpdateAPIView`
    * **Permission:** `IsAuthenticated` (Strict)
    * **Behavior:** Allows authenticated users to modify an existing book.
    * **Custom Hooks:** Includes `perform_update` to handle custom logic during object updates.

* **DeleteView (`/books/delete/<int:pk>/`):**
    * **Type:** `generics.DestroyAPIView`
    * **Permission:** `IsAuthenticated` (Strict)
    * **Behavior:** Allows authenticated users to remove a book.

### Testing Instructions
1.  **Read Access:** `GET /books/` (Available to everyone).
2.  **Write Access:** `POST /books/create/` (Requires authentication token or session).