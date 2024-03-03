# basic/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
# from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import requests 
from .forms import ContactForm

# Create your views here.

def index(request):
    form = ContactForm()  # Initialize an empty form
    # Pass form and contact_messages to the template context
    return render(request, "index.html", {'form': form})

# New view for handling the contact form submission

def handle_contact_form(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_data = form.cleaned_data
            fastapi_url = f'{settings.FASTAPI_BASE_URL}/contacts/'
            try:
                response = requests.post(fastapi_url, json=contact_data)
                if response.status_code == 200:
                    # Success: Return a JSON response indicating success
                    return JsonResponse({'success': True})
                else:
                    # Error from FastAPI: Return a JSON response with error message
                    return JsonResponse({'success': False, 'message': 'Failed to submit form to FastAPI.'})
            except requests.exceptions.RequestException as e:
                # Network or connection error: Return a JSON response with error message
                return JsonResponse({'success': False, 'message': f'An error occurred: {str(e)}'})
        else:
            # Form validation failed: Return form errors in JSON response
            errors = {field: errors[0] for field, errors in form.errors.items()}
            return JsonResponse({'success': False, 'errors': errors})

    else:
        form = ContactForm()

    return render(request, 'index.html', {'form': form})
