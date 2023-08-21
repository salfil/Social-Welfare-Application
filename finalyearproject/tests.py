from django.test import TestCase, Client
from django.urls import reverse, resolve
from unittest.mock import patch
from django.utils import timezone
from .models import Post, Comment
from datetime import datetime, timedelta
import datetime
from .forms import CommentForm
import json
from . import views
from .forms import PostForm, CommentForm, PostEditForm, ProgrammeForm 
from .forms import AppointmentForm, AcceptAppointmentForm, DeclineAppointmentForm, RearrangeAppointmentForm, UserAcceptAppointmentForm, CompleteAppointmentForm, CancelAppointmentForm
from django.contrib.auth.models import User, Group
from .models import Post, Category,  Comment, Staff, Programme, ProgrammeType, AppointmentBooking, User
from .forms import PostForm, CommentForm, PostEditForm, ProgrammeForm 
from .forms import AppointmentForm, AcceptAppointmentForm, DeclineAppointmentForm, RearrangeAppointmentForm, UserAcceptAppointmentForm, CompleteAppointmentForm, CancelAppointmentForm
from .views import HomeView, PostDetailView, ProgrammeDetailView, AddPostView, CategoryView, CategoryListView, AddCommentView
from .views import UpdatePostView, DeletePostView, LikeView, AddProgrammeView,  ProgrammesPageView, ProgrammeTypePageView, search_programmes
from . views import AllProgrammesPageView, view_appointments_view, Book_Appointment_View, AllStaffPageView, AppointmentDetailView
from . views import Appointment_Success_View, search_address, AcceptAppointmentView, search_appointment, DeclineAppointmentView, RearrangeAppointmentView, delete_appointment_user
from .views import UserAcceptAppointmentView, CompleteAppointmentView, completed_appointments_view,  CancelAppointmentView, search_appointments
from datetime import date
from django.test import TestCase, SimpleTestCase

#TESTING ALL MODELS
class TestModels(TestCase):
    def setUp(self):

        self.client=Client()

        #ALL THE MOCK DATA
        self.programme_type_1 = ProgrammeType.objects.create(type='health')
        self.programme_type_2 = ProgrammeType.objects.create(type='Social Skills')
        self.programme_type_3 = ProgrammeType.objects.create(type='workshop')

        self.user_1 = User.objects.create_user('w', 'w@example.com', 'password')
        self.user_2 = User.objects.create_user('e', 'e@example.com', 'password')

        self.programme_1 = Programme.objects.create(title='A', type=self.programme_type_1.type, description='X', link='https://hello.com', author=self.user_1)
        self.programme_2 = Programme.objects.create(title='B', type=self.programme_type_2.type, description='BBB', link='https://hello.com', author=self.user_2)

        self.category_1 = Category.objects.create(name='General')
        self.category_2 = Category.objects.create(name='Mental health')

        self.appointment_1 = AppointmentBooking.objects.create(first_name='Bob', last_name='Steve', description='Appointment description', app_date=date.today(), app_time='10:00', email='e@example.com', phone='1234567890', in_person=True, staff='Staff 1', key='22222', location='Location 1')
        self.appointment_2 = AppointmentBooking.objects.create(first_name='Joohn', last_name='X', description='Appointment description', app_date=date.today(), app_time='11:00', email='t@example.com', phone='1234567890', in_person=False, staff='Staff 2', key='22223', completed=True, location='Location 2')

        self.post_1 = Post.objects.create(title='Post 1', author=self.user_1, body='Post body 1', category=self.category_1.name)
        self.post_2 = Post.objects.create(title='Post 2', author=self.user_2, body='Post body 2', category=self.category_2.name)

        self.comment_1 = Comment.objects.create(post=self.post_1, name='A', body='Comment body 1')
        self.comment_2 = Comment.objects.create(post=self.post_2, name='B', body='Comment body 2')

        self.staff_1 = Staff.objects.create(user=self.user_1, speciality='Social Work', bio='Staff bio', linkedin_url='https://www.linkedin.com/', location='Location 1', full_name='A A')
        self.staff_2 = Staff.objects.create(user=self.user_2, speciality='Mspecialityt', bio='Staff bio', linkedin_url='https://www.linkedin.com/', location='Location 2', full_name='A B')

    #TEST CASES
    def test_staff(self):
        self.assertEqual(str(self.staff_1.user), 'w')
        self.assertEqual(str(self.staff_2.user), 'e')

    def test_staff_model_get_absolute_url(self):
        url = reverse('home')
        self.assertEqual(self.staff_1.get_absolute_url(), url)
        self.assertEqual(self.staff_2.get_absolute_url(), url)
    
    def test_staff_fields(self):
        staff_1 = Staff.objects.get(id=1)
        staff_2 = Staff.objects.get(id=2)
        self.assertEqual(self.staff_1.speciality, staff_1.speciality)
        self.assertEqual(self.staff_2.speciality, staff_2.speciality)
        self.assertEqual(self.staff_1.bio, staff_1.bio)
        self.assertEqual(self.staff_2.bio, staff_2.bio)
        self.assertEqual(self.staff_1.linkedin_url, staff_1.linkedin_url)
        self.assertEqual(self.staff_2.linkedin_url, staff_2.linkedin_url)
        self.assertEqual(self.staff_1.location, staff_1.location)
        self.assertEqual(self.staff_2.location, staff_2.location)
        self.assertEqual(self.staff_1.full_name, staff_1.full_name)
        self.assertEqual(self.staff_2.full_name, staff_2.full_name)
    
    def test_programme_type(self):
        programme_type = ProgrammeType.objects.get(id=1)
        self.assertEquals(str(programme_type), programme_type.type)
    
    def test_category(self):
        category = Category.objects.get(id=1)
        self.assertEquals(str(category), category.name)
    
    def test_programme(self):
        programme = Programme.objects.get(id=1)
        self.assertEqual(str(self.programme_1), programme.title)

    def test_programme_type_field(self):
        programme_1 = Programme.objects.get(id=1)
        programme_2 = Programme.objects.get(id=2)
        self.assertEqual(self.programme_1.type, programme_1.type)
        self.assertEqual(self.programme_2.type, programme_2.type)

    def test_programme_author_field(self):
        self.assertEqual(self.programme_1.author, self.user_1)
        self.assertEqual(self.programme_2.author, self.user_2)
    
    def test_comment(self):
        comment = Comment.objects.get(id=1)
        self.assertEqual(comment.post.title, self.post_1.title)
        self.assertEqual(comment.name, self.comment_1.name)
        self.assertEqual(comment.body, self.comment_1.body)

    def test_appointment_booking(self):
        appointment_1 = AppointmentBooking.objects.get(id=1)
        appointment_2 = AppointmentBooking.objects.get(id=2)
        self.assertEqual(str(appointment_1), self.appointment_1.first_name)
        self.assertEqual(str(appointment_2), self.appointment_2.first_name)
    
    def test_post_category(self):
        post_1 = Post.objects.get(id=1)
        post_2 = Post.objects.get(id=2)
        self.assertEqual(post_1.category, self.post_1.category)
        self.assertEqual(post_2.category, self.post_2.category)


#TEST CASES FOR ALL VIEWS
class TestViews(TestCase):

    def setUp(self):
        self.client=Client()

        #ALL MOCK DATA
        programme_type_1 = ProgrammeType.objects.create(type='health')
        programme_type_2 = ProgrammeType.objects.create(type='Social Skills')

        user_1 = User.objects.create_user('w', 'w@example.com', 'password')
        user_2 = User.objects.create_user('e', 'e@example.com', 'password')

        programme_1 = Programme.objects.create(title='A', type=programme_type_1.type, description='X', link='https://hello.com', author=user_1)
        programme_2 = Programme.objects.create(title='B', type=programme_type_2.type, description='BBB', link='https://hello.com', author=user_2)

        category_1 = Category.objects.create(name='General')
        category_2 = Category.objects.create(name='Mental health')

        appointment_1 = AppointmentBooking.objects.create(first_name='Bob', last_name='Steve', description='Appointment description', app_date=date.today(), app_time='10:00', email='e@example.com', phone='1234567890', in_person=True, staff='Staff 1', key='22222', location='Location 1')
        appointment_2 = AppointmentBooking.objects.create(first_name='Joohn', last_name='X', description='Appointment description', app_date=date.today(), app_time='11:00', email='t@example.com', phone='1234567890', in_person=False, staff='Staff 2', key='22223', completed=True, location='Location 2')

        
        post_1 = Post.objects.create(title='Post 1', author=user_1, body='Post body 1', category=category_1.name)
        post_2 = Post.objects.create(title='Post 2', author=user_2, body='Post body 2', category=category_2.name)

        
        comment_1 = Comment.objects.create(post=post_1, name='A', body='Comment body 1')
        comment_2 = Comment.objects.create(post=post_2, name='B', body='Comment body 2')

       
        staff_1 = Staff.objects.create(user=user_1, speciality='Social Work', bio='Staff bio', linkedin_url='https://www.linkedin.com/', location='Location 1', full_name='A A')
        staff_2 = Staff.objects.create(user=user_2, speciality='Mspecialityt', bio='Staff bio', linkedin_url='https://www.linkedin.com/', location='Location 2', full_name='A B')

    #TEST CASES
    def test_home(self):
        client = self.client
        response=client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
    
    def test_post_detail(self):
        response=self.client.get(reverse('post_detail', args=['1']))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_detail.html')
    
    def test_programme_detail(self):
        response=self.client.get(reverse('programme_detail', args=['1']))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'programme_detail.html')
    
    def test_add_post(self):
        client = self.client
        response=client.get(reverse('add_post'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_post.html')
    
    def test_category(self):
        response=self.client.get(reverse('category', args=['1']))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'categories.html')
    
    def test_add_post(self):
        client = self.client
        response=client.get(reverse('add_post'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_post.html')
    
    def test_category_list(self):
        client = self.client
        response=client.get(reverse('category_list'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'category_list.html')
    
    def test_add_comment(self):
        client = self.client
        response=client.get(reverse('add_comment', args=['1']))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_comment.html')
    
    def test_update_post(self):
        client = self.client
        response=client.get(reverse('update_post', args=['1']))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_post.html')
    
    def test_delete_post(self):
        client = self.client
        response=client.get(reverse('delete_post', args=['1']))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_post.html')
    
    def test_add_programme(self):
        response=self.client.get(reverse('add_programme'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_programme.html')
    
    def test_ProgrammesPage(self):
        response=self.client.get(reverse('programmesPage'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'programmes.html')
    
    def test_programme_type(self):
        client = self.client
        response=client.get(reverse('programme_type', args=['1']))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'programme_types.html')
    
    def test_search_programmes(self):
        response=self.client.get(reverse('search_programmes'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_programmes.html')
    
    def test_search_address(self):
        response=self.client.get(reverse('search_address'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_address.html')
    
    def test_search_appointment(self):
        response=self.client.get(reverse('search_appointment'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_appointment.html')
    
    def test_search_appointments(self):
        response=self.client.get(reverse('search_appointments'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_appointments.html')
    
    def test_all_programmes(self):
        response=self.client.get(reverse('all_programmes'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'all_programmes.html')
    
    def test_view_appointments(self):
        response=self.client.get(reverse('view_appointments'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_appointments.html')
    
    def test_book_appointment(self):
        client = self.client
        response=client.get(reverse('book_appointment'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_appointment.html')
    
    def test_all_staff(self):
        client = self.client
        response=client.get(reverse('all_staff'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'all_staff_members.html')
    
    def test_appointment_detail(self):
        client = self.client
        response=client.get(reverse('appointment_detail', args=['1']))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointment_detail.html')
    
    def test_delete_appointment(self):
        client = self.client
        response=client.get(reverse('delete_appointment', args=['1']))
        self.assertEquals(response.status_code, 302)
    
    def test_delete_appointment_user(self):
        client = self.client
        response=client.get(reverse('delete_appointment_user', args=['1']))
        self.assertEquals(response.status_code, 302)
    
    def test_route(self):
        client = self.client
        response=client.get(reverse('route'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'route.html')
    
    def test_accept_appointment(self):
        client = self.client
        response=client.get(reverse('accept_appointment', args=['1']))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accept_appointment.html')
    
    def test_accept_appointment_user(self):
        client = self.client
        response=client.get(reverse('accept_appointment_user', args=['1']))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accept_appointment_user.html')
    
    def test_decline_appointment(self):
        client = self.client
        response=client.get(reverse('decline_appointment', args=['1']))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'decline_appointment.html')
    
    def test_rearrange_appointment(self):
        client = self.client
        response=client.get(reverse('rearrange_appointment', args=['1']))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'rearrange_appointment.html')
    
    def test_complete_appointment(self):
        client = self.client
        response=client.get(reverse('complete_appointment', args=['1']))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'complete_appointment.html')
    
    def test_completed_appointments(self):
        client = self.client
        response=client.get(reverse('completed_appointments'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'completed_appointments.html')
    
    def test_cancel_appointment(self):
        client = self.client
        response=client.get(reverse('cancel_appointment', args=['1']))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cancel_appointment.html')

# TESTING ALL THE URLS BEING SUCCESSFULLY RESOLVED.
class TestUrls(SimpleTestCase):

    def test_home_url_is_resolved(self):
        url = reverse('home')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, HomeView)
    
    def test_post_detail_url_is_resolved(self):
        url = reverse('post_detail', args=['1'])
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, PostDetailView)
    
    def test_programme_detail_url_is_resolved(self):
        url = reverse('programme_detail', args=['1'])
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, ProgrammeDetailView)
    
    def test_add_post_url_is_resolved(self):
        url = reverse('add_post')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, AddPostView)
    
    def test_category_url_is_resolved(self):
        url = reverse('category', args=['1'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, CategoryView)
    
    def test_categorylist_url_is_resolved(self):
        url = reverse('category_list')
        print(resolve(url))
        self.assertEquals(resolve(url).func, CategoryListView)

    def test_addcomment_url_is_resolved(self):
        url = reverse('add_comment', args=['1'])
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, AddCommentView)
    
    def test_updatepost_url_is_resolved(self):
        url = reverse('update_post', args=['1'])
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, UpdatePostView)
    
    def test_deletepost_url_is_resolved(self):
        url = reverse('delete_post', args=['1'])
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, DeletePostView)
    
    def test_addprogramme_url_is_resolved(self):
        url = reverse('add_programme')
        self.assertEquals(resolve(url).func.view_class, AddProgrammeView)

    def test_programmesPage_url_is_resolved(self):
        url = reverse('programmesPage')
        self.assertEquals(resolve(url).func, ProgrammesPageView)

    def test_programmetype_url_is_resolved(self):
        url = reverse('programme_type', args=['test-programme'])
        self.assertEquals(resolve(url).func, ProgrammeTypePageView)

    def test_searchprogrammes_url_is_resolved(self):
        url = reverse('search_programmes')
        self.assertEquals(resolve(url).func, search_programmes)

    def test_searchaddress_url_is_resolved(self):
        url = reverse('search_address')
        self.assertEquals(resolve(url).func, search_address)

    def test_searchappointment_url_is_resolved(self):
        url = reverse('search_appointment')
        self.assertEquals(resolve(url).func, search_appointment)

    def test_searchappointments_url_is_resolved(self):
        url = reverse('search_appointments')
        self.assertEquals(resolve(url).func, search_appointments)

    def test_allprogrammes_url_is_resolved(self):
        url = reverse('all_programmes')
        self.assertEquals(resolve(url).func, AllProgrammesPageView)

    def test_viewappointments_url_is_resolved(self):
        url = reverse('view_appointments')
        self.assertEquals(resolve(url).func, view_appointments_view)

    def test_bookappointment_url_is_resolved(self):
        url = reverse('book_appointment')
        self.assertEquals(resolve(url).func.view_class, Book_Appointment_View)

    def test_allstaff_url_is_resolved(self):
        url = reverse('all_staff')
        self.assertEquals(resolve(url).func, AllStaffPageView)

    def test_appointment_detail_url_is_resolved(self):
        url = reverse('appointment_detail', args=[1])
        self.assertEquals(resolve(url).func.view_class, AppointmentDetailView)

    def test_delete_appointment_url_is_resolved(self):
        url = reverse('delete_appointment', args=['1'])
        self.assertEquals(resolve(url).func, views.delete_appointment)
        
    def test_deleteappointment_user_url_is_resolved(self):
        url = reverse('delete_appointment_user', args=['1'])
        self.assertEquals(resolve(url).func, views.delete_appointment_user)
        
    def test_route_url_is_resolved(self):
        url = reverse('route')
        self.assertEquals(resolve(url).func, views.route)
        
    def test_map_url_is_resolved(self):
        url = reverse('map')
        self.assertEquals(resolve(url).func, views.map)
        
    def test_acceptappointment_url_is_resolved(self):
        url = reverse('accept_appointment', args=['1'])
        self.assertEquals(resolve(url).func.view_class, AcceptAppointmentView)
        
    def test_acceptAppointmentUser_url_is_resolved(self):
        url = reverse('accept_appointment_user', args=['1'])
        self.assertEquals(resolve(url).func.view_class, UserAcceptAppointmentView)
        
    def test_declineappointment_url_is_resolved(self):
        url = reverse('decline_appointment', args=['1'])
        self.assertEquals(resolve(url).func.view_class, DeclineAppointmentView)
        
    def test_rearrangeappointment_url_is_resolved(self):
        url = reverse('rearrange_appointment', args=['1'])
        self.assertEquals(resolve(url).func.view_class, RearrangeAppointmentView)
        
    def test_completeappointment_url_is_resolved(self):
        url = reverse('complete_appointment', args=['1'])
        self.assertEquals(resolve(url).func.view_class, CompleteAppointmentView)
        
    def test_completedappointments_url_is_resolved(self):
        url = reverse('completed_appointments')
        self.assertEquals(resolve(url).func, completed_appointments_view)
        
    def test_cancelAppointment_url_is_resolved(self):
        url = reverse('cancel_appointment', args=['1'])
        self.assertEquals(resolve(url).func.view_class, CancelAppointmentView)








