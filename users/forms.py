from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from finalyearproject.models import Staff

#class based form for staff member to input details regarding their profile page. 
class ProfilePageForm(forms.ModelForm):

    class Meta:
        model = Staff
        #below are the fields belonging to the Staff object model that will be udated. 
        fields = ('bio', 'profile_pic', 'speciality', 'linkedin_url', 'location')
        widgets = {
            'bio': forms.TextInput(attrs={'class' : 'form-control'}),
            'speciality': forms.TextInput(attrs={'class' : 'form-control'}),
            'linkedin_url': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),

        }
        
#class based form for the staff member to create an account. 
class SignUpForm(UserCreationForm):
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class' : 'form-control'}))
    first_name=forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    last_name=forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    # Initializes a SignUpForm instance
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        # Adds 'form-control' class attribute to the widget of the relevant fields
        self.fields['username'].widget.attrs['class']= 'form-control'
        self.fields['password1'].widget.attrs['class']= 'form-control'
        self.fields['password2'].widget.attrs['class']= 'form-control'


#class based form for the staff member to edit their account details
class EditProfileForm(UserChangeForm):
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class' : 'form-control'}))
    first_name=forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    last_name=forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    username=forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    #account details corresponds to these 4 fields
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
