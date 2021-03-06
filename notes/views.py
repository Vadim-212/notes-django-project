from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.template.loader import get_template

from notes import templates
from notes.models import Note#, User
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from notes.forms import RegisterForm, LoginForm, NoteForm
from django.utils.translation import gettext as _
import logging


# Create your views here.


log = logging.getLogger(__name__)


def index(request):
    user_login = request.session.get('logged_user', None)
    return render(request, 'index.html', context={'user_login': user_login})

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
                    # print(user)
                    request.session['logged_user'] = user
                    # return HttpResponse('Authenticated successfully')
                    return redirect('index')
                else:
                    # return HttpResponse('Disabled account')
                    return render(request, 'signin.html', context={'form': form, 'error_message': _('Disabled account')})
            else:
                # return HttpResponse('Invalid login')
                return render(request, 'signin.html', context={'form': form, 'error_message': _('Invalid login or password')})
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
            htmly = get_template('confirm_email.html')
            d = {'username': username}
            subject, from_email, to = _('Email confirmation '), 'your@email', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            ##################################################################
            messages.success(request, f'Your account has been created ! You are now able to log in')
            # print(raw_password)
            user = authenticate(username=username, password=raw_password)
            # login(request, user)
            # new_user = login(username, email, raw_password)
            request.session['logged_user'] = user
            # print('\n\n------>', request.session['logged_user'])
            # print('--->', new_user, new_user.id, new_user.login, new_user.email, new_user.password)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'signup.html', context={'form': form})


def logout(request):
    if request.session.get('logged_user', None) is None:
        return redirect('index')
    del request.session['logged_user']
    return redirect('index')


def show_user(request):
    user_login = request.session.get('logged_user', None)
    if user_login is None:
        return redirect('index')
    user = User.objects.get(username=user_login)
    return render(request, 'show_user.html', context={'user': user})


def show_note(request, note_id):
    note = Note.objects.get(pk=note_id)
    if not note.is_private:
        return render(request, 'show_note.html', context={'note': note})
    if request.session.get('logged_user', None) is None:
        return redirect('index')
    return render(request, 'show_note.html', context={'note': note})


def show_user_notes(request):
    user_login = request.session.get('logged_user', None)
    if user_login is None:
        return redirect('index')
    user = User.objects.get(username=user_login)
    notes = Note.objects.filter(user=user).values('id','text','is_private','time_added')
    # print(notes[0])
    return render(request, 'show_user_notes.html', context={'notes': notes})


def add_note(request):
    if request.session.get('logged_user', None) is None:
        return redirect('index')
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            is_private = form.cleaned_data.get('is_private')
            text = form.cleaned_data.get('text')
            user = User.objects.get(username=request.session['logged_user'])
            note = Note(is_private=is_private, text=text, user=user)
            # print(note)
            note.save()
            # print('--->', new_user, new_user.id, new_user.login, new_user.email, new_user.password)
            return redirect('show_note', note_id=note.id)
    else:
        form = NoteForm()
    return render(request, 'add_note.html', context={'form': form})


def edit_note(request, note_id):
    if request.session.get('logged_user', None) is None:
        return redirect('index')
    note = Note.objects.filter(pk=note_id).first()
    if note is None:
        return redirect('index')
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            # form.save()
            is_private = form.cleaned_data.get('is_private')
            text = form.cleaned_data.get('text')
            # updated_note = Note.objects.get(pk=note_id)
            # updated_note.text = text
            # updated_note.is_private = is_private
            Note.objects.filter(id=note_id).update(is_private=is_private,text=text)
            # user = User.objects.get(username=request.session['logged_user'])
            # note = Note(is_private=is_private, text=text, user=user)
            # updated_note.save()
            # print('-->', updated_note.id)
            # print('--->', new_user, new_user.id, new_user.login, new_user.email, new_user.password)
            return redirect('show_note', note_id=note_id)
    else:
        form = NoteForm(initial={'is_private': note.is_private,'text': note.text})
    return render(request, 'edit_note.html', context={"form": form})


def del_note(request, note_id):
    if request.session.get('logged_user', None) is None:
        return redirect('index')
    note = Note.objects.filter(pk=note_id).first()
    if note is None:
        return redirect('index')
    note = Note.objects.filter(pk=note_id).delete()
    # print('-->', note)
    # note.delete()
    return redirect('show_user_notes')
