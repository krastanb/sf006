from django.urls import path 

from .views import * 

urlpatterns = [
    path('news', NewsList.as_view(), name='news'),
    path('articles', ArticleList.as_view(), name='articles'),
    path('<int:pk>', PostDetail.as_view(), name='newsid')
]