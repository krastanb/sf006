from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post
from .filters import NewsFilter

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


# Create your views here.
