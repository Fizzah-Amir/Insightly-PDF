from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
     path(
        "api/documents/",
        include("docs.urls")
    ),
    path(
        "api/questions/",
        include("questions.urls")
    ),
    path('api-auth/', include(
        'rest_framework.urls'
    )),
    path("accounts/", include("django.contrib.auth.urls")),
    path("app/", include("config.web_urls")),
    path("", RedirectView.as_view(pattern_name="web_document_list", permanent=False)),
     path("api/users/", include("users.urls")),
     
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )