from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name = 'user-register'),
    path('logout/', views.logout_view, name = 'user-logout'),
    path('logoutpage/', views.deconnexion, name = 'user-logoutpage'),
    path('profil/', views.profil, name = 'user-profile'),
    path('profil/update/', views.profil_update, name = 'user-profile_update'),
]
