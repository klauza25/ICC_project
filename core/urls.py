from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "ICC Management"
admin.site.site_title = "ICC Admin Portal"
admin.site.index_title = "Gestion de l'église ICC"


def home_redirect(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Redirection intelligente selon le rôle
    if request.user.role == 'admin':
        return redirect('chef_dashboard')  # Admin voit aussi le dashboard chef
    elif request.user.role == 'chef':
        return redirect('chef_dashboard')
    else:  # serviteur
        return redirect('serviteur_dashboard')


urlpatterns = [
    path('gestion-icc/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('attendance/', include('attendance.urls')),
    path('', home_redirect, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
