from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('create_project/', views.create_project, name='create_project'),
    path('vote/', views.vote, name='vote'),
    path('get_stats/<str:pid>', views.get_stats, name='get_stats'),
    path('get_project_data/<str:pid>', views.get_project_data, name='get_project_data'),
    path('get_report/<str:pid>', views.get_report, name='get_report')
]
