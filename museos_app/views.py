from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    context= {
        'museums': Museum.objects.all()
    }
    return render (request, "index.html", context)

def signup(request):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if errors:
            for e in errors.values():
                messages.error(request, e)
            return redirect('/signup')
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        User.objects.create(first_name=first_name, last_name=last_name, email=email, password=pw_hash)
        return redirect('/login')
    return render(request, 'signup.html')

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        if not User.objects.authenticate(email, password):
            messages.error(request, 'Invalid email/password')
            return redirect('/login')
        user = User.objects.get(email=email)
        request.session['user_id'] = user.id
        return redirect('/')
    return render(request, 'login.html')

def logout(request):
    print(request.session)
    request.session.flush()
    print(request.session)
    return redirect('/')