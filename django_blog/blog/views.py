from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in immediately after registration
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        user.email = request.POST.get('email')
        user.save()
        return redirect('profile')
    return render(request, 'blog/profile.html')

# 1. List View: Shows all posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-published_date'] # Newest first

# 2. Detail View: Shows one post
class PostDetailView(DetailView):
    model = Post
    # Default template: blog/post_detail.html

# 3. Create View: Allows creating new posts
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    # Default template: blog/post_form.html

    # Override form_valid to set the author automatically
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# 4. Update View: Allows editing posts
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    # Default template: blog/post_form.html (shared with CreateView)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # Ensure only the author can edit
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# 5. Delete View: Allows deleting posts
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/posts/' # Redirect here after deletion
    # Default template: blog/post_confirm_delete.html

    # Ensure only the author can delete
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author