from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Idea, Comment, News
from .forms import IdeaForm, CommentForm
from django.core.paginator import Paginator
from django.utils import timezone

def home(request):
    news_list = News.objects.order_by('-published_at')[:5]
    latest_ideas = Idea.objects.order_by('-created_at')[:5]
    context = {
        'news_list': news_list,
        'latest_ideas': latest_ideas,
    }
    return render(request, 'home.html', context)

def idea_list(request):
    ideas = Idea.objects.order_by('-created_at')
    paginator = Paginator(ideas, 10)  # По 10 идей на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'idea_list.html', {'page_obj': page_obj})

def idea_detail(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    comments = idea.comments.order_by('-created_at')
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.idea = idea
            comment.author = request.user
            comment.created_at = timezone.now()
            comment.save()
            return redirect('idea_detail', pk=idea.pk)
    else:
        comment_form = CommentForm()
    context = {
        'idea': idea,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'idea_detail.html', context)

@login_required
def idea_create(request):
    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.author = request.user
            idea.created_at = timezone.now()
            idea.save()
            return redirect('idea_detail', pk=idea.pk)
    else:
        form = IdeaForm()
    return render(request, 'idea_form.html', {'form': form})

def news_list(request):
    news = News.objects.order_by('-published_at')
    paginator = Paginator(news, 10)  # По 10 новостей на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news_list.html', {'page_obj': page_obj})

def news_detail(request, pk):
    news_item = get_object_or_404(News, pk=pk)
    return render(request, 'news_detail.html', {'news_item': news_item})

def search_ideas(request):
    query = request.GET.get('q')
    ideas = Idea.objects.filter(title__icontains=query) | Idea.objects.filter(description__icontains=query)
    paginator = Paginator(ideas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'idea_list.html', {'page_obj': page_obj, 'query': query})


# main_app/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

class CustomLogoutView(View):
    def post(self, request, *args, **kwargs):
        # Пайдаланушыны жүйеден шығару логикасы
        return HttpResponseRedirect(reverse_lazy('home'))


from django.shortcuts import get_object_or_404, redirect
from .models import Idea



def like_idea(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)
    if request.user.is_authenticated:
        if request.user in idea.likes.all():
            idea.likes.remove(request.user)
        else:
            idea.likes.add(request.user)
    return redirect('idea_detail', pk=idea_id)  # 'pk' параметрін қолданыңыз



from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from .models import Idea
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class IdeaDetailView(DetailView):
    model = Idea
    template_name = 'idea_detail.html'  # Шаблон файлының аты
    context_object_name = 'idea'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.all()  # Идеяға байланысты пікірлерді көрсету
        return context



from django.views.generic import DetailView
from .models import Idea

class IdeaDetailView(DetailView):
    model = Idea
    template_name = 'idea_detail.html'
    http_method_names = ['get']
