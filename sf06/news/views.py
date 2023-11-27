from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import NewsFilter
from .forms import AddPostForm

class NewsList(ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новости'
        context['filterset'] = self.filterset
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(type='NE')
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs


class ArticleList(ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Статьи'
        return context

    def get_queryset(self):
        return super().get_queryset().filter(type='AR')


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

class PostCreate(CreateView):
    form_class = AddPostForm
    model = Post
    template_name = 'postedit.html'
    def form_valid(self, form):
        post = form.save(commit=False)
        post.type='NE' if 'news' in self.request.path else 'AR'
        return super().form_valid(form)

class PostEdit(UpdateView):
    form_class = AddPostForm
    model = Post
    template_name = 'postedit.html'

class PostDelete(DeleteView):
    model = Post
    template_name = 'postedit.html'
    def get_success_url(self):
        return reverse_lazy('news') if 'news' in self.request.path else reverse_lazy('articles')
