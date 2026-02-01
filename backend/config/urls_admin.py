from django.contrib import admin
from django.urls import include, path

urlpatterns = [path("finances/", include("finances.urls_admin")), path("", admin.site.urls)]
