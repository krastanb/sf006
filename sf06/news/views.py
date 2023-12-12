from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Post, Category, Subscription
from .filters import NewsFilter
from .forms import AddPostForm
from .tasks import hello


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
        print('rdy')
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

class PostCreate(PermissionRequiredMixin, CreateView):
    form_class = AddPostForm
    permission_required = ('news.add_post')
    model = Post
    template_name = 'postedit.html'
    def form_valid(self, form):
        post = form.save(commit=False)
        post.type='NE' if 'news' in self.request.path else 'AR'
        return super().form_valid(form)

class PostEdit(PermissionRequiredMixin, UpdateView):
    form_class = AddPostForm
    permission_required = ('news.change_post')
    model = Post
    template_name = 'postedit.html'

class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    permission_required = ('news.delete_post')
    template_name = 'postedit.html'
    def get_success_url(self):
        return reverse_lazy('news') if 'news' in self.request.path else reverse_lazy('articles')

@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        cat_id = request.POST.get('category_id')
        category = Category.objects.get(id=cat_id)
        action = request.POST.get('action')
        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(user=request.user, category=category).delete()
    categories = Category.objects.annotate(user_is_subs=Exists(Subscription.objects.filter(user=request.user, category=OuterRef('pk'))))
    return render(request, 'subscriptions.html', {'cats':categories})