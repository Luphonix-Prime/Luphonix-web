from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('team/', views.TeamView.as_view(), name='team'),
    path('technologies/', views.TechnologiesView.as_view(), name='technologies'),
    path('projects/', views.ProjectsView.as_view(), name='projects'),
    path('contact/', views.ContactView.as_view(), name='contact'),
]
