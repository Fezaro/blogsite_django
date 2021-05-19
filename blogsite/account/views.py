from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile

# Create your views here.

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST) # instantiate form
        if form.is_valid(): # check whether form is valid
            cd = form.cleaned_data # clean form data
            user = authenticate(request, username=cd["username"], password=cd['password']) #authenticate against db
            if  user is not None:
                if user.is_active: # checks if authenticated user is active 
                    login(request,user)# returns user object 
                    return HttpResponse("Authenticated successfully")
                else:
                    return HttpResponse("Disabled account")
            else:
                return HttpResponse('Invalid Login')
    else:
        form = LoginForm() # if method is GET . Form is instantiated
        return render(request, "account/login.html", {'form':form})

@login_required
def dashboard(request):
    return render(request,'account/dashboard.html', {'section': 'dashboard'})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # create a new user object but avoid saving it yet
            new_user= user_form.save(commit=False)
            # Set the password chosen by user
            # we use the set_password() method of the User model to encrypt
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the user object 
            new_user.save()
            # Create user profile
            return render(request,'account/register_done.html', {'user_form': user_form})
    else:
        user_form = UserRegistrationForm()

    return render(request,'account/register.html', {'user_form': user_form})

@login_required # needs authentication
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.Profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid:
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})
