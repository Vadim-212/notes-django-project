from django.shortcuts import render, redirect
from notes import templates
from notes.models import Note#, User
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from notes.forms import RegisterForm, LoginForm
from django.utils.translation import gettext as _
import logging


# Create your views here.


log = logging.getLogger(__name__)


def index(request):
    try:
        print('session ->', request.session['logged_user'])
    except Exception as e:
        print(e)
    return render(request, 'index.html', context={'request': request})

# LoginView
# LoginView
# LoginView
# check method "login" (django.contrib.auth.__init__.py)
def sign_in(request):
    # user = User.objects.get()
    # request.session['logged_user_id'] = user.id
    # return render(request, 'signin.html')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            # User.objects.get()
            if user is not None:
                if user.is_active:
                    login(request, user)
                    print(user)
                    request.session['logged_user'] = user
                    # return HttpResponse('Authenticated successfully')
                    return redirect('index')
                else:
                    # return HttpResponse('Disabled account')
                    return render(request, 'signin.html', context={'form': form, 'error_message': _('Disabled account')})
            else:
                # return HttpResponse('Invalid login')
                return render(request, 'signin.html', context={'form': form, 'error_message': _('Invalid login')})
    else:
        form = LoginForm()
    return render(request, 'signin.html', context={'form': form})


def sign_up(request):
    # user = User()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            # print(raw_password)
            user = authenticate(username=username, password=raw_password)
            # login(request, user)
            # new_user = login(username, email, raw_password)
            request.session['logged_user'] = user
            print('\n\n------>', request.session['logged_user'])
            # print('--->', new_user, new_user.id, new_user.login, new_user.email, new_user.password)
            return redirect('index')
    else:
        form = RegisterForm()

    return render(request, 'signup.html', context={'form': form})


def logout(request):
    del request.session['logged_user']
    return redirect('index')


def show_user(request):
    try:
        user_id = request.session['logged_user']
    except:
        return redirect('index')
    user = User.objects.get(username=user_id)
    return render(request, 'show_user.html', context={'user': user})