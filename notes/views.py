from django.shortcuts import render, redirect
from notes import templates
from notes.models import Note, User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from notes.forms import RegisterForm, login, LoginForm


# Create your views here.


def index(request):
    print('session ->', request.session['logged_user_id'])
    return render(request, 'index.html')


def sign_in(request):
    # user = User.objects.get()
    # request.session['logged_user_id'] = user.id
    # return render(request, 'signin.html')
    # if request.method == 'POST':
    #     form = LoginForm(request.POST)
    #     if form.is_valid():
    #         username = form.cleaned_data.get('username')
    #         password = form.cleaned_data.get('password')
    #         user = authenticate(username=username, password=password)
    #         User.objects.get()
    #         if user is not None:
    #             if user.is_active:
    #                 login(request, user)
    #                 return HttpResponse('Authenticated successfully')
    #             else:
    #                 return HttpResponse('Disabled account')
    #         else:
    #             return HttpResponse('Invalid login')
    # else:
    #     form = LoginForm()
    return render(request, 'account/login.html')#, {'form': form})


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
            # login(request, user.id)
            new_user = login(username, email, raw_password)
            request.session['logged_user_id'] = new_user.id
            # print('--->', new_user, new_user.id, new_user.login, new_user.email, new_user.password)
            return redirect(index)
    else:
        form = RegisterForm()
    # request.session['logged_user_id'] = user.id
    return render(request, 'signup.html', context={'form': form})


def logout(request):
    del request.session['logged_user_id']
    return redirect('index')


def show_user(request):
    user_id = request.session['logged_user_id']
    user = User.objects.get(pk=user_id)
    return render(request, 'show_user.html', context={'user': user})