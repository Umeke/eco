
from .models import Idea, Comment



from django import forms
from .models import Idea

class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ['title', 'description', 'category']  # category өрісі көрсетілгеніне көз жеткізіңіз

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


