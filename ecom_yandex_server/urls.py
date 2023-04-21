from django.urls import path
from .views import serve_site_files, new_action

urlpatterns = [
    path('new_action/', new_action),
    path('site/<path:path>', serve_site_files),
]
