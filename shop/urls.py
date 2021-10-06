from django.urls import path
from .views.auth import index,signIn, signOut, register_storeadmin, activate_storeadmin
from .views.shop import dashboard
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('login', signIn, name='login'),
    path('signOut', signOut, name='signOut'),
    path('register_storeadmin', register_storeadmin, name="register_storeadmin"),
    path('activate_storeadmin/<int:id>', activate_storeadmin, name="activate_storeadmin"),
    
    
    path('dashboard', dashboard, name='dashboard'),
   

]
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
