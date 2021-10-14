from django.urls import path
from .views.auth import activate_clerk, addclerk, index,signIn, signOut, register_storeadmin, activate_storeadmin,profile,updatepassword,update_profile,update_profilephoto,adminact_clerk,admindeact_clerk,delete_clerk,update_clerk
from .views.shop import dashboard, new_items, send_requests,storeadmin_requests
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('login', signIn, name='login'),
    path('signOut', signOut, name='signOut'),
    path('register_storeadmin', register_storeadmin, name="register_storeadmin"),
    path('activate_storeadmin/<int:id>', activate_storeadmin, name="activate_storeadmin"),
    path('activate_clerk/<int:id>',activate_clerk,name='activate_clerk'),
    path('addclerk',addclerk,name="addclerk"),
    path('dashboard', dashboard, name='dashboard'),

    path('profile', profile, name='profile'),
    path('updatepassword', updatepassword, name='updatepassword'),
    path('update_profile', update_profile, name='update_profile'),
    path('update_profilephoto', update_profilephoto, name='update_profilephoto'),   

    path('new_items', new_items, name='new_items'),
    path('send_requests', send_requests, name='send_requests'),
    
    path('adminact_clerk/<int:id>',adminact_clerk),
    path('admindeact_clerk/<int:id>',admindeact_clerk),
    path('delete_clerk/<int:id>',delete_clerk),
    path('update_clerk/<int:id>',update_clerk),
    path('storeadmin_requests',storeadmin_requests),

    

]
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
