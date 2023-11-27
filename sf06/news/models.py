from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


article = 'AR'
news = 'NE'
POSITIONS = [
    (article, 'Статья'),
    (news, 'Новость')
]

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rating = Post.objects.filter(author=self).aggregate(Sum('rating'))['rating__sum']*3  # рейтинг всех постов автора
        commentary_rating = Comment.objects.filter(user=self.user).aggregate(Sum('rating'))['rating__sum'] # рейтинг всех комментариев автора
        rating_by_comments_to_post = Comment.objects.filter(post__in=Post.objects.filter(author=self)).count() # рейтинг по количеству комментариев к постам автора 
        self.rating = post_rating + commentary_rating + rating_by_comments_to_post
        self.save()

    def __str__(self):
        return self.user.username

class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.category_name


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length = 2, choices=POSITIONS, default=article)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    header = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def get_absolute_url(self):
        if self.type=='NE':
            return reverse('newsid', args=(self.pk,))
        else:
            return reverse('articleid', args=(self.pk,))

    def preview(self):
        return f"{self.text[:124]}..."

    def like(self):
        self.rating+=1
        self.save()

    def dislike(self):
        self.rating-=1
        self.save()

    def __str__(self):
        return f'{self.header}' 


class PostCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating+=1
        self.save()

    def dislike(self):
        self.rating-=1
        self.save()