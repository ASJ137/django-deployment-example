from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileInfoForm

# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    return render(request,"basic_app/index.html")


def register(request):
    register = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()


            profile =profile_form.save(commit=False)
            profile.user =user

            if "profile_pic" in request.FILES:
                profile.profile_pic = request.FILES["profile_pic"]

            profile.save()
            register = True

        else:
            print(user_form.errors,profile_form.errors)


    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,"basic_app/registration.html",{"user_form":user_form,"profile_form":profile_form,"registered":register})


def user_login(request):

    if request.method == "POST":
        # First get the username and password supplied
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Django's built-in authentication function:
        user = authenticate(username=username,password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('index'))

            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")

        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'basic_app/login.html', {})


@login_required
def special(request):
    # Remember to also set login url in settings.py!
    # LOGIN_URL = '/basic_app/user_login/'
    return HttpResponse("You are logged in. Nice!")

@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('index'))
