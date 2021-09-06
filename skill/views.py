from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, "skill/index.html")



def python_skill(request):
    return render(request, "skill/python_skill.html")