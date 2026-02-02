from django.urls import path

from . import views

app_name = "integrations"

urlpatterns = [
    path("openai/generate-ideas/", views.OpenAIIdeaGeneratorView.as_view(), name="openai-generate-ideas"),
]
