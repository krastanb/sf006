from django.urls import path 

from .views import * 

urlpatterns = [
    path('news', NewsList.as_view(), name='news'),
    path('news/search', NewsList.as_view(), name='searchnews'),
    path('news/<int:pk>', PostDetail.as_view(), name='newsid'),
    path('news/create', PostCreate.as_view(), name='newscreate'),
    path('news/<int:pk>/edit', PostEdit.as_view(), name='newsedit'),
    path('news/<int:pk>/delete', PostDelete.as_view(), name='newsdelete'),

    path('articles', ArticleList.as_view(), name='articles'),
    path('articles/<int:pk>', PostDetail.as_view(), name='articleid'),
    path('articles/create', PostCreate.as_view(), name='articlecreate'),
    path('articles/<int:pk>/edit', PostEdit.as_view(), name='articleedit'),
    path('articles/<int:pk>/delete', PostDelete.as_view(), name='articledelete'),

    path('subscriptions', subscriptions, name='subscriptions'),
    
]