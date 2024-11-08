from django.urls import path
from . import views
from .views import like_idea

from .views import IdeaDetailView
urlpatterns = [
    path('', views.home, name='home'),
    path('ideas/', views.idea_list, name='idea_list'),
    path('ideas/<int:pk>/qwe', IdeaDetailView.as_view(), name='idea_detail'),
    path('ideas/<int:pk>/', views.idea_detail, name='idea_detail'),
    path('ideas/new/', views.idea_create, name='idea_create'),
    path('idea/<int:idea_id>/like/', like_idea, name='like_idea'),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('search/', views.search_ideas, name='search_ideas'),
    path('ideas/<int:pk>/', views.IdeaDetailView.as_view(), name='idea_detail'),

]
