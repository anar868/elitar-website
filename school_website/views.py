from django.shortcuts import render, redirect
from repo.teacher import Teacher
from repo.student import StudentClass
from repo.student_class import Class


def home_view(request):
    return redirect('add_missing')


def add_missing(request):
    return StudentClass.add_missing(request)


def user_login(request):
    return StudentClass.user_login(request)


def user_logout(request):
    return StudentClass.user_logout(request)


def remove_missing(request):
    return StudentClass.remove_missing(request)


def class_checked(request):
    return StudentClass.class_checked(request)


def class_list(request):
    return StudentClass.class_list(request)


def missing_students(request, class_id):
    return StudentClass.missing_students(request, class_id)


def add_user(request):
    return StudentClass.add_user(request)



