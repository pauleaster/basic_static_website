# basic/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
# from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import requests 
from .forms import ContactForm

# Create your views here.

def index(request):
    return render(request, "index.html")


# New view for handling the contact form submission

def submit_contact_form(request):
    if request.method == "POST":
        form = ContactForm(request.POST)  # Instantiate the form with POST data
        if form.is_valid():
            contact_data = form.cleaned_data  # Cleaned data is a dict of validated form input
            fastapi_url = f'{settings.FASTAPI_BASE_URL}/contacts/'
            try:
                # Send the data to FastAPI
                response = requests.post(fastapi_url, json=contact_data)
                if response.status_code == 200:
                    # If request is AJAX, return JSON response
                    if request.is_ajax():
                        return JsonResponse({"message": "Form submitted successfully to FastAPI."}, status=200)
                    else:
                        # Handle non-AJAX success (e.g., redirect or send a success message)
                        return HttpResponse("Form submitted successfully to FastAPI.")
                else:
                    if request.is_ajax():
                        return JsonResponse({"message": "Failed to submit form to FastAPI."}, status=400)
                    else:
                        # Handle non-AJAX failure
                        return HttpResponse("Failed to submit form to FastAPI.", status=400)
            except requests.exceptions.RequestException as e:
                if request.is_ajax():
                    return JsonResponse({"message": f"An error occurred: {str(e)}"}, status=500)
                else:
                    # Handle non-AJAX connection error
                    return HttpResponse(f"An error occurred: {str(e)}", status=500)
        else:
            # Form validation failed
            if request.is_ajax():
                return JsonResponse({"message": "Form validation failed.", "errors": form.errors.as_json()}, status=400)
            else:
                # Handle non-AJAX form validation failure (e.g., redirect back to form with errors)
                # Here, you might redirect back to the form page and display errors, but implementation details will vary
                return HttpResponse("Form validation failed.", status=400)
    else:
        # If not a POST request, redirect to the index page or show an error
        return redirect('index')