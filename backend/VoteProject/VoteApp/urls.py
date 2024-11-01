from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('create_project/', views.create_project, name='create_project'),
    path('vote/', views.vote, name='vote'),
]
