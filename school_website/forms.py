from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm

from school_website.models import Student, Class

import datetime


User = get_user_model()


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ['student_class']


def year_choices():
    return [(r, r) for r in reversed(range(1940, datetime.date.today().year + 1))]


def current_year():
    return datetime.date.today().year


class ClassForm(ModelForm):
    starting_year = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=current_year)

    class Meta:
        model = Class
        fields = ['class_name', 'grade_number', 'sector']


class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'student_class']
