from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, UserChangeForm 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import SignUpForm, EditProfileForm, ProfilePageForm 
from django.views.generic import DetailView, CreateView
from finalyearproject.models import Staff

#class based view for staff member to edit the profile page. 
class EditProfilePageView(generic.UpdateView):
    #Staff model is the model that will be updated. 
    model = Staff
    template_name = 'registration/edit_profile_page.html'
    #fields that the staff member has the options of editing 
    fields = ['bio', 'profile_pic', 'speciality', 'linkedin_url', 'location', 'full_name']
    #this is the url where the staff member will be directed to after completion
    success_url = reverse_lazy('home')

#class based view for staff member to create the profile page. 
class CreateProfilePageView(CreateView):
    model = Staff
    form_class = ProfilePageForm
    template_name = "registration/create_user_profile_page.html"
    
    
    def form_valid(self, form):
        #sets the user field of the form instance to the current user who is creating the profile page
        form.instance.user = self.request.user
        return super().form_valid(form)


#class based view to output the profile page. 
class ShowProfilePageView(DetailView):
    model = Staff
    template_name = 'registration/user_profile.html'

    def get_context_data(self, *args, **kwargs):
        staff = Staff.objects.all()
        #retrieve default context date
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        #retrieve the staff member with the corresponding primary key
        page_user=get_object_or_404(Staff, id=self.kwargs['pk'])
        context["page_user"] = page_user
        return context

# Class based view for staff member to register an account
class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name= 'registration/register.html'
    success_url=reverse_lazy('login')

#class based view for the staff member to edit their account information
class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name= 'registration/edit_profile.html'
    success_url=reverse_lazy('home')
    
    def get_object(self):
        return self.request.user



