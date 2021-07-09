from django.db import models
import re

from django.db.models.fields import DateTimeField

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors={}
        email_checker = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['pw']) < 8:
            errors['pw'] = "Your password must be at least 8 characters long."
        if len(postData['fname']) < 2 or len(postData['lname']) < 2:
            errors['name'] = "Your name must be at least 2 characters long."
        if not email_checker.match(postData['email']):
            errors['email'] = "You must enter a valid email."
        if postData['pw'] != postData['confpw']:
            errors['pw'] = "Your password and confirm password must match."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    objects = UserManager()

class Museum(models.Model):
    museum = models.CharField(max_length=50)
    price = models.FloatField()
    address = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.museum} {self.address} {self.price}"

class RatingManager(models.Manager):
    def validate_only_one_rating_per_museum_by_user(self, user, museum):
        for i in user.ratings.all():
            if i.museum.id == museum.id:
                print('GETS HERE')
                return False
        return True

class Rating(models.Model):
    rating = models.IntegerField()
    user = models.ForeignKey(User, related_name="ratings", on_delete=models.CASCADE)
    museum = models.OneToOneField(Museum, on_delete=models.CASCADE, primary_key=True)
    created_at = DateTimeField(auto_now_add=True, null=True)
    updated_at = DateTimeField(auto_now=True, null=True)
    objects = RatingManager()

class Opinion(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, related_name="opinions", on_delete=models.CASCADE)
    museum = models.OneToOneField(Museum, on_delete=models.CASCADE, primary_key=True)
    created_at = DateTimeField(auto_now_add=True, null=True)
    updated_at = DateTimeField(auto_now=True, null=True)