from datetime import datetime

from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy, resolve
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, PostCategory
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


class ProtectedView(LoginRequiredMixin, TemplateView):
    template_name = 'prodected_page.html'


class PostList(ListView):
    model = Post
    ordering = 'data'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     self.filterset = PostFilter(self.request.GET, queryset)
    #     return self.filterset.qs
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['time_now'] = datetime.utcnow()
    #     context['next_sale'] = None
    #     context['filterset'] = self.filterset
    #     context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
    #     return context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class SearchNews(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search_news'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.choice = 'NW'
        return super().form_valid(form)


class ArticlesCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'articles_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.choice = 'AT'
        return super().form_valid(form)


class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'


class ArticlesUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView,):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'articles_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class NewsDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class ArticlesDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/news')


class CategoryListView(ListView):
    model = Post
    template_name = 'category.html'
    context_object_name = 'category_news'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category)
        #        queryset = Post.objects.filter(category=self.category).order_by('-date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscribers'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    if not category.subscribers.filter(id=user.id).exists():
        category.subscribers.add(user)
        email = user.email
        html = render_to_string(
            'subscribed.html',
            {
                'categories': category,
                'user': user,
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'Вы подписались на категорию: {category}',
            body='Подписан',
            from_email='ildardave@yandex.ru',
            to=[email, ],
        )
        msg.attach_alternative(html, 'text/html')

        try:
            msg.send()
        except Exception as e:
            print(e)
    return redirect(request.META.get('HTTP_REFERER'))


