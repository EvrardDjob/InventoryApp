

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path("admin/", admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('user/', include('user.urls')),
    path('', auth_views.LoginView.as_view(template_name ='user/login.html', next_page='dashboard-index'), name = 'user-login'),
    #path('user/logout/', auth_views.LogoutView.as_view(template_name = 'user/logout.html'), name = 'user-logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name = 'user/password_reset.html'), name = 'password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name = 'user/password_reset_done.html'), name = 'password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'user/password_reset_confirm.html'), name = 'password_reset_confirm'),
    
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'user/password_reset_complete.html'), name = 'password_reset_complete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
