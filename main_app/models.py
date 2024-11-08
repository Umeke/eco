from django.db import models
from django.contrib.auth.models import User


class Idea(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100, blank=True, null=True)
    # Лайк өрісін қосу
    likes = models.ManyToManyField(User, related_name='liked_ideas', blank=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title


class Comment(models.Model):
    idea = models.ForeignKey(Idea, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Комментарий от {self.author}'

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)  # Қосымша уақыт өрісі

    def __str__(self):
        return self.title


from django.shortcuts import get_object_or_404, redirect
from .models import Idea

def like_idea(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)
    if request.user.is_authenticated:
        if request.user in idea.likes.all():
            idea.likes.remove(request.user)
        else:
            idea.likes.add(request.user)
    return redirect('idea_detail', idea_id=idea_id)  # 'idea_detail' - идеяның детальды көрінісінің аты

