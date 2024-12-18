from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]

from django.urls import include
from django.urls import path
urlpatterns += [
    path('BA/', include('BA.urls', namespace='BA')),
]


from django.views.generic import RedirectView
urlpatterns += [
    path('', RedirectView.as_view(url='/BA/', permanent=True)),
]

urlpatterns += [
path('accounts/', include('django.contrib.auth.urls')),
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
