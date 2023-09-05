from django.urls import path
from .views import PostList, PostDetail, NewsCreate, NewsUpdate, NewsDelete,\
   ArticlesCreate, ArticlesUpdate, ArticlesDelete

urlpatterns = [
   path('', PostList.as_view(),name='post_list'),
   path('<int:pk>', PostDetail.as_view(),name='post_detail'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='post_delete'),
   path('article/create', ArticlesCreate.as_view(), name='article_create'),
   path('article/<int:pk>/edit/', ArticlesUpdate.as_view(), name='article_update'),
   path('article/<int:pk>/delete/', ArticlesDelete.as_view(), name='post_delete'),
]