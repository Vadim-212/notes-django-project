from django.shortcuts import render, redirect
from notes import templates
from notes.models import Note, User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate


# Create your views here.


def index(request):
    return render(request, 'index.html')


def sign_in(request):
    user = User()
    request.session['logged_user_id'] = user.id
    return render(request, 'signin.html')


def sign_up(request):
    #user = User()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user.id)
            print(user)
            return redirect(index)
    else:
        form = UserCreationForm()
    #request.session['logged_user_id'] = user.id
    return render(request, 'signup.html', context={'form': form})


def logout(request):
    del request.session['logged_user_id']
    return redirect(index)


def show_user(request):
    user_id = request.session['logged_user_id']
    user = User.objects.get(pk=user_id)
    return render(request, 'show_user.html', context={'user': user})