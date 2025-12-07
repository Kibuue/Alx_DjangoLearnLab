# Django Blog Project (Alx_DjangoLearnLab)

## Project Overview
A full-featured blog application built with Django, following the MVT (Model-View-Template) architecture. This project serves as a learning lab for building web applications using Python and Django.

## Prerequisites
- Python 3.14.0
- Django 5.8.3

## Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone <repository_url>
    cd Alx_DjangoLearnLab
    ```

2.  **Set Up Virtual Environment**
    ```bash
    # Create virtual environment
    python -m venv venv

    # Activate virtual environment
    # Windows:
    venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install django
    ```

4.  **Database Migration**
    Apply the initial migrations to set up the database (SQLite) and the Blog models.
    ```bash
    cd django_blog
    python manage.py makemigrations blog
    python manage.py migrate
    ```

5.  **Run the Server**
    ```bash
    python manage.py runserver
    ```
    Access the application at: `http://127.0.0.1:8000/`

## Project Structure
```text
Alx_DjangoLearnLab/
├── venv/                   # Virtual environment
└── django_blog/            # Project Root
    ├── manage.py
    ├── db.sqlite3
    ├── django_blog/        # Project Configuration
    │   ├── settings.py     # Configured for static files and apps
    │   ├── urls.py
    │   └── ...
    └── blog/               # Main Blog Application
        ├── models.py       # Contains 'Post' model
        ├── templates/
        │   └── blog/
        │       └── base.html  # Base layout with navbar/footer
        └── static/
            ├── css/
            │   └── styles.css # Custom styling
            └── js/
                └── scripts.js # Custom JavaScript

- **Task 1:** Implemented User Authentication.
    - Created `CustomUserCreationForm` to capture emails.
    - Added Views for Register and Profile management.
    - Configured URLs for Login, Logout, Register, and Profile.
    - Added templates: `login.html`, `register.html`, `logout.html`, `profile.html`.
    - Secured forms with CSRF tokens.


- **Task 2:** Implemented CRUD functionality (Create, Read, Update, Delete).
    - Added `PostListView`, `PostDetailView`, `PostCreateView`, `PostUpdateView`, `PostDeleteView`.
    - Configured URL routing for posts (`/post/new/`, `/post/<pk>/`, etc.).
    - Implemented `LoginRequiredMixin` to protect views.
    - Implemented `UserPassesTestMixin` so only authors can edit/delete their own work.
    - Created CRUD templates: `post_list`, `post_detail`, `post_form`, `post_confirm_delete`.