from django.urls import path
from .views import PostList, PostDetail, NewsCreate, NewsUpdate, NewsDelete, \
   ArticlesCreate, ArticlesUpdate, ArticlesDelete, upgrade_me, IndexView, \
   CategoryListView, subscribe, SearchNews, main_page
from django.views.decorators.cache import cache_page

urlpatterns = [
   path('acc/', IndexView.as_view(), name='index'),
   path('', main_page),
   path('posts/', cache_page(60*5)(PostList.as_view()), name='posts_list'),
   path('search/', cache_page(60*5)(SearchNews.as_view()), name='search'),
   path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='post_delete'),
   path('article/create/', ArticlesCreate.as_view(), name='article_create'),
   path('article/<int:pk>/edit/', ArticlesUpdate.as_view(), name='article_update'),
   path('article/<int:pk>/delete/', ArticlesDelete.as_view(), name='post_delete'),
   path('upgrade/', upgrade_me, name='upgrade'),
   path('categories/<int:pk>', cache_page(60*5)(CategoryListView.as_view()), name='category'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),


]
