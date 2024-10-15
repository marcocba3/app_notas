from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('notas/', views.login_view, name='notes'),  # Asegúrate de que la vista se llame 'notes'
]
