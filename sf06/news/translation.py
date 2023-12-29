from .models import Category, Post
from modeltranslation.translator import translator, register, TranslationOptions # импортируем декоратор для перевода и класс настроек, от которого будем наследоваться

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('text','header')