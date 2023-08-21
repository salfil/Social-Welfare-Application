from django  import forms
from .models import Post, Category, Comment, User, Programme, ProgrammeType, AppointmentBooking
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms.widgets import SelectDateWidget
from django.contrib.auth.models import User
from django import forms
from finalyearproject.models import Staff
from datetime import datetime, time
import jwt
import requests
import json, random
from django.forms.widgets import SelectDateWidget
from django.core.exceptions import ValidationError
from django.utils import timezone


key=random.randrange(100)
#choices=[('General', 'General'), ('mental health','mental health' ), ('career', 'career')]

#list to output choices of list of categories. 
choices = Category.objects.all().values_list('name', 'name')
choice_list=[]
#list to output choices of types of programmes.
programme_types = ProgrammeType.objects.all().values_list('type', 'type')
programme_types_list=[]
#list to output choices of staff members. 
staff_members = User.objects.all().values_list('first_name', 'first_name')
staff_members_list=[]

#loop through all existing staff members and append it to the list. 
for staff in staff_members:
    staff_members_list.append(staff)

#loop through all existing programme types and append it to the list. 
for programme in programme_types:
    programme_types_list.append(programme)

#loop through all existing choices for categories and append it to the list. 
for choice in choices:
    choice_list.append(choice)

class LocationForm(forms.Form):
    location = forms.CharField(max_length=255)
    radius = forms.IntegerField()

#form which users will fill in to book an appointment. 
class AppointmentForm(forms.ModelForm):

    #staff member user will have appointment with
    staff = forms.TypedChoiceField(label='Staff Member')
    #styling the field onto the form. CSS class attribute of a form widget 
    staff.widget.attrs.update({'class': 'app-form-control'})
    app_time = forms.TypedChoiceField(label='Time of Appointment')  # time of appointment
    app_time.widget.attrs.update({'class': 'app-form-control'})
    in_person: forms.BooleanField()
    #random number output for the key
    key = forms.IntegerField(label=str(random.randrange(100000)) + ' is your key', widget=forms.TextInput(attrs={'placeholder': 'Key'}))
    key.widget.attrs.update({'class': 'app-form-control'})
   
    #meta class to generate fields from the model and describe behaviour of the form. 
    class Meta:
        model = AppointmentBooking
        fields = ('first_name', 'last_name', 'description', 'staff', 'app_date', 'app_time', 'email', 'phone', 'in_person', 'key')
    
        widgets = {
                'first_name': forms.TextInput(attrs={'class' : 'form-control'}),
                'last_name': forms.TextInput(attrs={'class' : 'form-control'}),
                #'author': forms.Select(attrs={'class' : 'form-control'}),
                'description': forms.Textarea(attrs={'class': 'form-control'}),
                #'staff': forms.TypedChoiceField(label='staff').widget.attrs.update({'class': 'app-form-control'}),
                #'staff': forms.Select(choices=staff_members_list,attrs={'class' : 'form-control'}),
                'app_date': forms.DateInput(attrs={'type': 'date', 'class' : 'form-control'}),
                'app_time': forms.DateInput(attrs={'type': 'time', 'class' : 'form-control'}),
                'email':  forms.EmailInput(attrs={'class' : 'form-control'}),
                'phone': forms.TextInput(attrs={'class' : 'form-control'}),
                
            }
    
    #output relevant data and lists for the user to choose from for staff member and times
    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        #self.fields['key'].choices = [str(random.randrange(100)) ]
        self.fields['staff'].choices = staff_members_list
        self.fields['app_time'].choices = [('9:00', '9:00'), ('10:00', '10:00'), ('11:00', '11:00'),
                                           ('13:00', '13:00'), ('14:00', '14:00'), ('15:00', '15:00'),
                                           ('16:00', '16:00'), ('17:00', '17:00')]
    
    
    #clean method to perform validation of date and time selection
    def clean(self):
        cleaned_data = super().clean()
        staff = cleaned_data.get('staff')
        app_date = cleaned_data.get('app_date')
        app_time_str = cleaned_data.get('app_time')
    
        # Convert app_time_str to a datetime.time object
        app_time = datetime.strptime(app_time_str, '%H:%M').time()

        #checks if the user accidently tries to book an appointment at a date that has already passed. 
        if datetime.combine(app_date, app_time) < datetime.now():
            raise ValidationError('You cannot book an appointment in the past.')

        # Check if there is any appointment booking with the same date and time
        if AppointmentBooking.objects.filter(staff=staff, app_date=app_date, app_time=app_time).exists():
            raise ValidationError('An appointment is already booked at this date and time.')
        
        #If there is no conflict, it returns the result
        return cleaned_data
        
#form for staff member to post a programme. 
class ProgrammeForm(forms.ModelForm):
    class Meta:
        model = Programme
        fields = ('title', 'author', 'type', 'description', 'link')

        widgets = {
            'title': forms.TextInput(attrs={'class' : 'form-control'}),
            #'author': forms.Select(attrs={'class' : 'form-control'}),
            'author': forms.TextInput(attrs={'class' : 'form-control', 'value':'', 'id':'e', 'type':'hidden'}),
            'type': forms.Select(choices=programme_types_list,attrs={'class' : 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'link': forms.TextInput(attrs={'class' : 'form-control'}),
        }

#form for staff members to create a post
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'author','category', 'body', 'header_image')

        widgets = {
            'title': forms.TextInput(attrs={'class' : 'form-control'}),
            #'author': forms.Select(attrs={'class' : 'form-control'}),
            'author': forms.TextInput(attrs={'class' : 'form-control', 'value':'', 'id':'e', 'type':'hidden'}),
            'category': forms.Select(choices=choice_list,attrs={'class' : 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }

#form for staff members to edit their post. 
class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','category', 'body')

        widgets = {
            'title': forms.TextInput(attrs={'class' : 'form-control'}),
            #'author': forms.Select(attrs={'class' : 'form-control'}),
            #'author': forms.TextInput(attrs={'class' : 'form-control', 'value':'', 'id':'elder', 'type':'hidden'}),
            'category': forms.Select(choices=choice_list,attrs={'class' : 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }

#form for staff members to accept appointment
class AcceptAppointmentForm(forms.ModelForm):

    accepted: forms.BooleanField()

    class Meta:
        model = AppointmentBooking
        fields = ('link','accepted', 'location')

        widgets = {
            'link': forms.TextInput(attrs={'class' : 'form-control'}),
            'location': forms.TextInput(attrs={'class' : 'form-control'}),
        }

#form for users to accept an appointment
class UserAcceptAppointmentForm(forms.ModelForm):

    user_accepted: forms.BooleanField(label='accept?')

    class Meta:
        model = AppointmentBooking
        fields = ('user_accepted',)

#form for staff member to complete an appointment
class CompleteAppointmentForm(forms.ModelForm):

    completed: forms.BooleanField(label='Complete?')

    class Meta:
        model = AppointmentBooking
        fields = ('completed',)

#form to cancel an appointment
class CancelAppointmentForm(forms.ModelForm):

    cancelled: forms.BooleanField(label='Cancel?')

    class Meta:
        model = AppointmentBooking
        fields = ('cancelled',)
       
#form to decline an appointment
class DeclineAppointmentForm(forms.ModelForm):

    declined: forms.BooleanField()

    class Meta:
        model = AppointmentBooking
        fields = ('declined','message')

        widgets = {
            'message': forms.TextInput(attrs={'class' : 'form-control'}),
        }

#form to rearrange an appointment
class RearrangeAppointmentForm(forms.ModelForm):

    rearranged: forms.BooleanField()
    app_time = forms.TypedChoiceField(label='Time of Appointment')  # time of appointment
    app_time.widget.attrs.update({'class': 'app-form-control'})

    class Meta:
        model = AppointmentBooking
        #only the date, time and rearranged fields are used here from the model as only these fields will be changed.
        fields = ('rearranged','app_date','app_time')

        widgets = {
            'app_date': forms.DateInput(attrs={'type': 'date', 'class' : 'form-control'}),
            'app_time': forms.DateInput(attrs={'type': 'time', 'class' : 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(RearrangeAppointmentForm, self).__init__(*args, **kwargs)
        self.fields['app_time'].choices = [('9:00', '9:00'), ('10:00', '10:00'), ('11:00', '11:00'),
                                           ('13:00', '13:00'), ('14:00', '14:00'), ('15:00', '15:00'),
                                           ('16:00', '16:00'), ('17:00', '17:00')]


#form to post a comment on a post
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body')

        widgets = {
            'name': forms.TextInput(attrs={'class' : 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }

