from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

posts = [
    {
        'author':'Hitesh',
        'title':'Blog Post1',
        'content':'First Post Content',
        'date_posted':'July 17,2021'
    },
    {
        'author':'Ravi',
        'title':'Blog Post2',
        'content':'Second Post Content',
        'date_posted':'July 18,2021'
    }
]

# Create your views here.

def index(request):
    return render(request,'blog/index.html', {
        'posts':Post.objects.all()
    })

class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'     # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    #paginate_by =2

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post=self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post=self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html')

