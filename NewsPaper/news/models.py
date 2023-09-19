from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from django.core.validators import MinValueValidator


class Author(models.Model):
    user_author = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)

    def update_rating(self):
        rating_posts_author = Post.objects.filter(author=self).aggregate(Sum('post_rating')).get(
            'post_rating__sum') * 3
        rating_comments_author = Comment.objects.filter(user=self.user_author).aggregate(Sum('comment_rating')).get(
            'comment_rating__sum')
        rating_comments_posts = Comment.objects.filter(user=self.id).aggregate(Sum('comment_rating')).get(
            'comment_rating__sum')

        self.user_rating = rating_posts_author + rating_comments_author + rating_comments_posts
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name.title()


class Post(models.Model):
    ARTICLE = 'AT'
    NEWS = 'NW'
    CHOICE = [(ARTICLE, 'Статья'), (NEWS, 'Новость')]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    choice = models.CharField(max_length=2, choices=CHOICE,default=NEWS)
    data = models.DateField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    header = models.CharField(max_length=64,)
    post_text = models.TextField(default='text')
    post_rating = models.IntegerField(default=0)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return self.post_text[:124]+'...'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(default='text')
    data = models.DateField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()




