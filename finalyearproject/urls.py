from django.contrib import admin
from django.urls import path, include
from . import views
from .views import HomeView, PostDetailView, ProgrammeDetailView, AddPostView, CategoryView, CategoryListView, AddCommentView
from .views import UpdatePostView, DeletePostView, LikeView, AddProgrammeView,  ProgrammesPageView, ProgrammeTypePageView, search_programmes
from . views import AllProgrammesPageView, view_appointments_view, Book_Appointment_View, AllStaffPageView, AppointmentDetailView
from . views import Appointment_Success_View, search_address, AcceptAppointmentView, search_appointment, DeclineAppointmentView, RearrangeAppointmentView, delete_appointment_user
from .views import UserAcceptAppointmentView, CompleteAppointmentView, completed_appointments_view,  CancelAppointmentView, search_appointments

#all the url patterns that point to  a particular view function which  will then point to a template to render the page
urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('post/<int:pk>', PostDetailView.as_view(), name="post_detail"),
    path('programme/<int:pk>', ProgrammeDetailView.as_view(), name="programme_detail"),
    path('add_post/', AddPostView.as_view(), name="add_post" ),
    path('category/<str:cats>/', CategoryView, name='category'),
    path('category_list/', CategoryListView, name='category_list'),
    path('post/<int:pk>/comment/', AddCommentView.as_view(), name="add_comment"),
    path('post/edit/<int:pk>', UpdatePostView.as_view(), name='update_post'), 
    path('post/<int:pk>/delete', DeletePostView.as_view(), name='delete_post'), 
    path('like/<int:pk>', LikeView, name='like_post'),
    path('add_programme', AddProgrammeView.as_view(), name='add_programme'),
    path('programmes', ProgrammesPageView, name='programmesPage'),
    path('type/<str:types>/', ProgrammeTypePageView, name='programme_type'),
    path('search_programmes', search_programmes, name='search_programmes'),
    path('search_address', search_address, name='search_address'),
    path('search_appointment', search_appointment, name='search_appointment'),
    path('search_appointments', search_appointments, name='search_appointments'),
    path('all_programmes', AllProgrammesPageView, name='all_programmes'),
    path('view_appointments', view_appointments_view, name='view_appointments'),
    path('book_appointment', Book_Appointment_View.as_view(), name='book_appointment'),
    path('all_staff', AllStaffPageView, name='all_staff'),
    path('appointment_detail/<int:pk>', AppointmentDetailView.as_view(), name='appointment_detail'),
    path('delete_appointment/<appointment_id>', views.delete_appointment, name='delete_appointment'),
    path('delete_appointment_user/<appointment_id>', views.delete_appointment_user, name='delete_appointment_user'),
    path('appointment_success/', Appointment_Success_View, name='appointment_success'),
    path('route', views.route, name="route"),
    path('map', views.map, name="map"),
    path('accept_appointment/<int:pk>', AcceptAppointmentView.as_view(), name='accept_appointment'),
    path('accept_appointment_user/<int:pk>', UserAcceptAppointmentView.as_view(), name='accept_appointment_user'),
    path('decline_appointment/<int:pk>', DeclineAppointmentView.as_view(), name='decline_appointment'),
    path('rearrage_appointment/<int:pk>', RearrangeAppointmentView.as_view(), name='rearrange_appointment'),
    path('complete_appointment/<int:pk>', CompleteAppointmentView.as_view(), name='complete_appointment'),
    path('completed_appointments', completed_appointments_view, name='completed_appointments'),
    path('cancel_appointment/<int:pk>', CancelAppointmentView.as_view(), name='cancel_appointment'),

]