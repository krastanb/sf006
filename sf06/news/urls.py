from django.urls import path 

from .views import * 

urlpatterns = [
    path('news/search', NewsList.as_view(), name='searchnews'),
    path('news', NewsList.as_view(), name='news'),
    path('articles', ArticleList.as_view(), name='articles'),
    path('news/<int:pk>', PostDetail.as_view(), name='newsid')
]