from django.urls import path
from .views import PostList, PostDetail, NewsCreate, NewsUpdate, NewsDelete, \
   ArticlesCreate, ArticlesUpdate, ArticlesDelete, upgrade_me, IndexView, \
   CategoryListView, subscribe, SearchNews

urlpatterns = [
   path('acc/', IndexView.as_view(),name='index'),
   path('posts/', PostList.as_view(),name='posts_list'),
   path('search/', SearchNews.as_view(), name='search'),
   path('<int:pk>/', PostDetail.as_view(),name='post_detail'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='post_delete'),
   path('article/create/', ArticlesCreate.as_view(), name='article_create'),
   path('article/<int:pk>/edit/', ArticlesUpdate.as_view(), name='article_update'),
   path('article/<int:pk>/delete/', ArticlesDelete.as_view(), name='post_delete'),
   path('upgrade/', upgrade_me, name='upgrade'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),


]
