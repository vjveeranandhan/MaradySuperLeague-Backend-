from user_manager.views import create_user, user_login, get_user,get_all_user ,update_user
from django.urls import path
from django.conf import settings  
from django.conf.urls.static import static  

urlpatterns = [
    path('create-user/', create_user, name='create_user'),
    path('user-login/', user_login, name='user_login'),
    path('get-user/', get_user, name='get_user'),
    path('get-all-user/', get_all_user, name='get_all_user'),
    path('update-user/', update_user, name='update_user'),
]

if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  