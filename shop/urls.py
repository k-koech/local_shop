from django.urls import path
from .views.auth import index,signIn, signOut
from .views.dashboard import dashboard
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('login', signIn, name='login'),
    path('signOut', signOut, name='signOut'),

    path('dashboard', dashboard, name='dashboard'),
   

]
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
