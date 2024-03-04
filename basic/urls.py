"""basic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path(
        "django/",
        include(
            [
                path("", views.index, name="index"),
                path("skill/", include("skill.urls")),
                path("admin/", admin.site.urls),
                path('accounts/', include('django.contrib.auth.urls')), 
                path(
                    "functions/handle_contact_form",
                    views.handle_contact_form,
                    name="handle_contact_form",
                ),
                path("oauth/", include("oauth2_provider.urls", namespace="oauth2_provider")),
                path("functions/login", views.login_view, name="login"),
                path("oauth/callback/", views.oauth_callback, name="oauth_callback"),
            ]
        ),
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
