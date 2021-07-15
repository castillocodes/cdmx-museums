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
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        password = request.POST['pw']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        User.objects.create(first_name=first_name, last_name=last_name, email=email, password=pw_hash)
        return redirect('/login')
    return render(request, 'signup.html')

# def login(request):
#     if request.method == "POST":
#         email = request.POST['email']
#         password = request.POST['pw']
#         if not User.objects.authenticate(email, password):
#             messages.error(request, 'Invalid email/password')
#             return redirect('/login')
#         user = User.objects.get(email=email)
#         request.session['user_id'] = user.id
#         return redirect('/')
#     return render(request, 'login.html')

def login(request):
    if request.method == 'POST':
        logged_user = User.objects.filter(email = request.POST['email'])
        if logged_user:
            logged_user = logged_user[0]
            if bcrypt.checkpw(request.POST['pw'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                request.session['user_fname'] = logged_user.first_name
                request.session['user_lname'] = logged_user.last_name
                return redirect('/dashboard')
            else:
                return render(request, 'login.html')
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')     
                    
def signout(request):
    print(request.session)
    request.session.flush()
    print(request.session)
    return redirect('/')

def rate(request, id):
    if not 'user_id' in request.session:
        messages.error(request, "You must be logged in to rate and give your opinion.")
        return redirect(request.META["HTTP_REFERER"])
    user_to_validate = User.objects.get(id=request.session['user_id'])
    museum_to_rate = Museum.objects.get(id=id)
    if not Rating.objects.validate_only_one_rating_per_museum_by_user(user_to_validate, museum_to_rate):
        messages.error(request, "You have already rated & opined this museum.")
        return redirect(request.META["HTTP_REFERER"])
    context = {
        "museum": museum_to_rate
    }
    return render(request, 'rate_and_comment.html', context)

def add_rating(request, id):
    if request.method == "POST":
        museum_to_rate = Museum.objects.get(id=id)
        user_id = request.session['user_id']
        opinion = request.POST['opinion']
        user = User.objects.get(id=user_id)
        Opinion.objects.create(text=opinion, user=user, museum=museum_to_rate)
        rating = request.POST['rating']
        Rating.objects.create(rating=rating, user=user, museum=museum_to_rate)
        return redirect('/dashboard')
    return redirect('/')

def dashboard(request):
    user = User.objects.get(id=request.session['user_id'])
    all_museums = Museum.objects.all()
    all_opinions = Opinion.objects.all()
    context = {
        "user" : user,
        "all_museums" : all_museums,
        "all_opinions" : all_opinions,
        "museums": Museum.objects.all()
    }
    return render(request, 'dashboard.html', context)

def edit_rating_opinion(request, museum_id):
    museum = Museum.objects.get(id=museum_id)
    museum_rating = Rating.objects.get(museum=museum)
    museum_opinion = Rating.objects.get(museum=museum)
    context = {
        "rating": museum_rating,
        "opinion": museum_opinion
    }
    return render(request, 'edit_opinion.html', context)

def modify_edit_opinion(request):
    if request.method == "POST":
        edited_rating = request.POST['rating']
        edited_opinion = request.POST['opinion']
        museum_id = request.POST['museum_id']
        museum = Museum.objects.get(id=museum_id)
        user = User.objects.get(id=request.session['user_id'])
        rating_query = Rating.objects.filter(museum=museum).filter(user=user)
        rating = rating_query[0]
        opinion_query = Opinion.objects.filter(museum=museum).filter(user=user)
        opinion = opinion_query[0]
        print('Rating to delete:', rating.__dict__)
        print('Rating to delete:', opinion.__dict__)

        rating.rating = edited_rating
        rating.save()
        opinion.text = edited_opinion
        opinion.save()
    return redirect('/')

def rate_feed(request):
    all_ratings = Rating.objects.all()
    all_opinions = Opinion.objects.all()
    context = {
        "all_ratings" : all_ratings,
        "all_opinions" : all_opinions
    }
    return render(request, 'rate_feed.html', context)

def delete_rating(request, id):
    museum = Museum.objects.get(id=id)
    user = User.objects.get(id=request.session['user_id'])
    rating_query = Rating.objects.filter(museum=museum).filter(user=user)
    rating = rating_query[0]
    opinion_query = Opinion.objects.filter(museum=museum).filter(user=user)
    opinion = opinion_query[0]
    print('Rating to delete:', rating.__dict__)
    print('Opinion to delete:', opinion.__dict__)
    rating.delete()
    opinion.delete()
    return redirect(request.META["HTTP_REFERER"])