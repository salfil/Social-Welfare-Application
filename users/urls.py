from django.contrib import admin
from django.urls import path, include
from . import views
from .views import UserRegisterView,UserEditView, ShowProfilePageView, EditProfilePageView, CreateProfilePageView 

#url patterns that point to the view function which will in point to the template for rendering
urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    #path('register/client/', views.register_client_view, name='register_client'),
    path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
    path('<int:pk>/staff', ShowProfilePageView.as_view(), name='show_profile_page'),
    path('<int:pk>/staff', ShowProfilePageView.as_view(), name='show_profile_page'),
    path('<int:pk>/edit_staff_page', EditProfilePageView.as_view(), name='edit_profile_page'),
    path('create_profile_page', CreateProfilePageView.as_view(), name='create_profile_page'),
]