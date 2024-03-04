# basic/views.py

from urllib.parse import urlencode
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

def login_view(request):
    auth_url_base = "http://localhost:8000/django/oauth/authorize/"
    params = {
        "response_type": "code",
        "client_id": settings.BASIC_OAUTH_CLIENT_ID,
        "redirect_uri": settings.BASIC_OAUTH_REDIRECT_URI,
    }
    
    # Construct full authorization URL
    full_auth_url = f"{auth_url_base}?{urlencode(params)}"
    print(f"Full auth URL:\n {full_auth_url}")

    # Pass the full authorization URL to the template
    context = {'auth_url': full_auth_url}
    return render(request, 'login.html', context)

def oauth_callback(request):
    code = request.GET.get('code')
    error = request.GET.get('error')
    print(f"Code: {code}, Error: {error}")

    if error:
        # Handle the error case appropriately.
        return JsonResponse({'error': error})

    if code:
        # Exchange the authorization code for an access token.
        token_url = 'http://localhost:8000/django/oauth/token/'
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': settings.BASIC_OAUTH_CLIENT_ID,
            'client_secret': settings.BASIC_OAUTH_CLIENT_SECRET,  # Assumes you've added this to your settings
            'redirect_uri': settings.BASIC_OAUTH_REDIRECT_URI,  # Make sure this is consistent
        }
        response = requests.post(token_url, data=data)

        if response.status_code == 200:
            # Handle success - you might want to store the access token, depending on your application's needs
            access_token = response.json().get('access_token')
            return JsonResponse({'access_token': access_token})
        else:
            # Handle failure to obtain access token
            return JsonResponse({'error': 'Failed to retrieve access token'}, status=response.status_code)

    # If no code or error is provided, it's an unexpected state.
    return JsonResponse({'error': 'No authorization code provided'}, status=400)