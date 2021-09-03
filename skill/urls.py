from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('python_skill', views.python_skill, name = 'python_skill'),
    
]