from django.contrib import admin
from .models import Author, Post, Comment, Category, PostCategory, Subscription
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline

# class PostCategories(admin.TabularInline):
#     model = PostCategory
#     extra = 2
#
# class PostAdmin(admin.ModelAdmin):
#     inlines = (PostCategories,)

class PostAdmin(TranslationAdmin):
    model = Post
class CategoryAdmin(TranslationAdmin):
    model = Category


admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Subscription)

# Register your models here.



