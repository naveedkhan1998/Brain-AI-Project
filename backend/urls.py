from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.views.generic import TemplateView
from . import settings

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("",  include("main.urls")),
        path("__reload__/", include("django_browser_reload.urls")),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.OUTPUT_URL, document_root=settings.OUTPUT_ROOT)
)
