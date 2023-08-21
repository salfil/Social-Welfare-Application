from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category,  Comment, Staff, Programme, ProgrammeType, AppointmentBooking
from .forms import PostForm, CommentForm, PostEditForm, ProgrammeForm 
from .forms import AppointmentForm, AcceptAppointmentForm, DeclineAppointmentForm, RearrangeAppointmentForm, UserAcceptAppointmentForm, CompleteAppointmentForm, CancelAppointmentForm
from django.contrib.auth.models import User, Group

from django.urls import reverse_lazy, reverse

from django.http import HttpResponseRedirect

from django.shortcuts import render
from django.conf import settings

# Create your views here.
from django.shortcuts import render
from django.conf import settings

from .directions import Directions

#view function for routing functionality. 
def route(request):
    #key passed into the template. 
	context = {"google_api_key": settings.GOOGLE_API_KEY}
	return render(request, 'route.html', context)


#view to display the map and directions. 
def map(request):

	lat_a = request.GET.get("lat_a")
	long_a = request.GET.get("long_a")
	lat_b = request.GET.get("lat_b")
	long_b = request.GET.get("long_b")
    #calls Directions method to calculate directions based on given parameters
	directions = Directions(
		lat_a= lat_a,
		long_a=long_a,
		lat_b = lat_b,
		long_b=long_b
		)

	context = {
	"google_api_key": settings.GOOGLE_API_KEY,
	"lat_a": lat_a,
	"long_a": long_a,
	"lat_b": lat_b,
	"long_b": long_b,
	"origin": f'{lat_a}, {long_a}',
	"destination": f'{lat_b}, {long_b}',
	"directions": directions,

	}
	return render(request, 'map.html', context)


#def home(request):
#    return render(request, 'home.html', {})
def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post_detail'), 
    args=[str(pk)])

#view function for the home page
class HomeView(ListView):
    model = Post
    template_name='home.html'
    #ordering = ['-id']
    ordering = ['-post_date']
    cats=Category.objects.all()

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context

#view function for list of categories
def CategoryListView(request):
    #get all of the categories using the all() method
    cat_menu_list = Category.objects.all()
    #pass variable onto the template to render the page
    return render(request, 'category_list.html', {'cat_menu_list': cat_menu_list,})

#view function to view posts of a certain category.
def CategoryView(request, cats):
    #filter posts of a particular category
    category_posts = Post.objects.filter(category=cats)
    return render(request, 'categories.html', {'cats': cats, 
    'category_posts':category_posts})

#view function to ouput particular programmes
def ProgrammeTypePageView(request, types):
    programme_types = Programme.objects.filter(type=types)
    return render(request, 'programme_types.html', {'types': types, 
    'programme_types':programme_types})

#view function to output programme types 
def ProgrammesPageView(request):
    programmes= ProgrammeType.objects.all()
    return render(request, 'programmes.html', {'programmes': programmes}) 

#view function to output all the programmes. 
def AllProgrammesPageView(request):
    all_programmes= Programme.objects.all()
    return render(request, 'all_programmes.html', {'programmes': all_programmes})

def view_appointments_view(request):
    #order_by method makes sure appointments are ordered appropriately
    all_appointments = AppointmentBooking.objects.all().order_by('app_date', 'app_time')
    return render(request, 'view_appointments.html', {'appointments' : all_appointments})

#For appointments that have been marked as complete. 
def completed_appointments_view(request):
    #get appointments that are completed. 
    all_appointments = AppointmentBooking.objects.get(completed=True)
    return render(request, 'completed_appointments.html', {'appointments' : all_appointments})

# This function deletes an appointment from the database based on its ID.
def delete_appointment(request, appointment_id):
    # Retrieve the appointment object using the specified ID.
    appointment = AppointmentBooking.objects.get(pk=appointment_id)
    # Delete the appointment object.
    appointment.delete()
    # Redirect the user to the view appointments page.
    return redirect('view_appointments')

# This function is similar to the previous one, but redirects the user to the book appointment page instead.
def delete_appointment_user(request, appointment_id):
    # Retrieve the appointment object using the specified ID.
    appointment = AppointmentBooking.objects.get(pk=appointment_id)
    # Delete the appointment object.
    appointment.delete()
    # Redirect the user to the book appointment page.
    return redirect('book_appointment')

# This function renders the appointment_success.html template.
def Appointment_Success_View(request):
    return render(request, 'appointment_success.html')

# This function retrieves all staff members from the database and renders the all_staff_members.html template.
def AllStaffPageView(request):
    # Retrieve all staff objects from the database.
    staffs= Staff.objects.all()
    # Render the all_staff_members.html template, passing in the staffs variable as context data.
    return render(request, 'all_staff_members.html', {'staffs': staffs})

#View function for user to search for their particular appointment. 
def search_appointment(request):
    if request.method == "POST":
        #fetch what they user has searched. 
        searched = request.POST.get('searched', "appointment")
        searched = request.POST['searched']
        #filter method to only output appointment details for the specified key. 
        appointments=AppointmentBooking.objects.filter(key__contains=searched)
        #passes result to the template to output the information
        return render(request, 'search_appointment.html', {'searched': searched, 
        'appointments':appointments})
    else:
        return render(request, 'search_appointment.html', {}) 

#View function for user to search all of their appointments. 
def search_appointments(request):
    if request.method == "POST":
        #fetch what they user has searched. 
        searched = request.POST.get('searched', "appointment")
        searched = request.POST['searched']
        #filter method to only output appointments of user with specified phone number. 
        appointments=AppointmentBooking.objects.filter(phone__contains=searched)
        #passes result to the template to output the appointments. 
        return render(request, 'search_appointments.html', {'searched': searched, 
        'appointments':appointments})
    else:
        return render(request, 'search_appointments.html', {}) 

# This function searches for User objects that match the first name containing the specified search term.
def search_address(request):
    if request.method == "POST":
        # Retrieve the search term from the POST data.
        searched = request.POST.get('searched', "hello")
        searched = request.POST['searched']
        # Search for User objects that match the search term.
        staffs = User.objects.filter(first_name__contains=searched)
        # Render the search_address.html template, passing in the search term and the matching User objects as context data.
        return render(request, 'search_address.html', {'searched': searched, 'staffs':staffs})
    else:
        # Render the search_address.html template with an empty context if no search term was provided.
        return render(request, 'search_address.html', {})

# This view function allows the user to search for programmes
def search_programmes(request):
    if request.method == "POST":
        # Retrieve the search term from the POST data.
        searched = request.POST.get('searched')
        searched = request.POST['searched']
        # Search for Programme objects that match the search term.
        programmes = Programme.objects.filter(title__contains=searched)
        # Render the search_programmes.html template, passing in the search term and the matching Programme objects as context data.
        return render(request, 'search_programmes.html', {'searched': searched, 'programmes':programmes})
    else:
        # Render the search_programmes.html template with an empty context if no search term was provided.
        return render(request, 'search_programmes.html', {})

# View function to ouput the details regarding each programme 
class ProgrammeDetailView(DetailView):
    # Set the model to use for this view.
    model = Programme
    # Set the template to use for this view.
    template_name = 'programme_detail.html'

    # Add extra context data to the template.
    def get_context_data(self, *args, **kwargs):
        # Retrieve all Programme objects.
        programme_menu = Programme.objects.all()
        # Call the superclass implementation of get_context_data() and add the programme_menu variable to the context.
        context = super(ProgrammeDetailView, self).get_context_data(*args, **kwargs)
        context["programme_menu"] = programme_menu
        # Return the updated context data.
        return context

#view function as a class to output details about selected appointment
class AppointmentDetailView(DetailView):
    model = AppointmentBooking
    template_name = 'appointment_detail.html'
    form_class= AcceptAppointmentForm

    #method to get information regarding selected appointment. 
    def get_context_data(self, *args, **kwargs):
        #gets all instances of that object. 
        appointments = AppointmentBooking.objects.all()
        #gets all the relevant information regarding a particular appointment booking once selected. 
        context = super(AppointmentDetailView, self).get_context_data(*args, **kwargs)
        context["appointments"] = appointments
        return context
    
#class based view to output details of what the staff member has posted
class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

    #method to get information regarding the post 
    def get_context_data(self, *args, **kwargs):
        #get all instances of the Categories
        cat_menu = Category.objects.all()
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context

#class based view which outputs form for the user to book an appointment
class Book_Appointment_View(CreateView):
    model = AppointmentBooking
    template_name = 'book_appointment.html'
    form_class= AppointmentForm

    '''def get_context_data(self, *args, **kwargs):
        staffs = Staff.objects.all()
        context = super(Book_Appointment_View, self).get_context_data(*args, **kwargs)
        context["staffs"] = staffs
        return context'''

#class based view for staff member to  add a programme. 
class AddProgrammeView(CreateView):
    model = Programme
    form_class=ProgrammeForm
    template_name = 'add_programme.html'

#class based view for staff member to  add a post. 
class AddPostView(CreateView):
    model = Post
    form_class=PostForm
    template_name ='add_post.html'

#class based view for staff member to update a post. 
class UpdatePostView(UpdateView):
    model = Post
    form_class = PostEditForm
    template_name = 'update_post.html'
    
#class based view for staff member to accept an appointment. 
class AcceptAppointmentView(UpdateView):
    model = AppointmentBooking
    form_class = AcceptAppointmentForm
    template_name = 'accept_appointment.html'

#class based view for the user to accept an appointment. 
class UserAcceptAppointmentView(UpdateView):
    model = AppointmentBooking
    form_class = UserAcceptAppointmentForm
    template_name = 'accept_appointment_user.html'

#class based view for the user to decline an appointment.
#updateview is used as the models decline field will now be updated
class DeclineAppointmentView(UpdateView):
    model = AppointmentBooking
    form_class = DeclineAppointmentForm
    template_name = 'decline_appointment.html'

#class based view for the user to complete an appointment.
class CompleteAppointmentView(UpdateView):
    model = AppointmentBooking
    form_class = CompleteAppointmentForm
    template_name = 'complete_appointment.html'

#class based view for the staff member to rearrange an appointment.
class RearrangeAppointmentView(UpdateView):
    model = AppointmentBooking
    form_class = RearrangeAppointmentForm
    template_name = 'rearrange_appointment.html'

#class based view to cancel an appointment.
class CancelAppointmentView(UpdateView):
    model = AppointmentBooking
    form_class = CancelAppointmentForm
    template_name = 'cancel_appointment.html'

#class based view to delete a post
class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    #returns to the home page once deletion is complete
    success_url = reverse_lazy("home")

#class based view to add a comment
class AddCommentView(CreateView):
    model = Comment
    form_class=CommentForm
    template_name ='add_comment.html'

    # This method is called when the form is successfully validated
    def form_valid(self, form):
        # We set the post_id field of the comment to the primary key of the post that the comment is related to
        form.instance.post_id = self.kwargs['pk']
        # We call the parent class's form_valid method to save the form
        return super().form_valid(form)

    # We specify the URL to redirect to after a successful form submission
    success_url = reverse_lazy('home')
