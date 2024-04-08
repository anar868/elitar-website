from django.db import models
from django.contrib.auth.models import AbstractUser

import datetime
from django.core.validators import MaxValueValidator, MinValueValidator


class Class(models.Model):
    class_name = models.CharField(max_length=5, blank=False, null=False)
    grade_number = models.IntegerField(blank=False, null=False)
    sector = models.CharField(max_length=50, choices=(
        ('Sektor',(
            ('Az', 'Az'),
            ('Rus', 'Rus'))
         ),
    ), default='Az', null=False, blank=False)

    def __str__(self):
        return self.class_name


class User(AbstractUser):
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE, null=True)


class Student(models.Model):
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name + " " + self.last_name


class MissingStudents(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.student.first_name + " " + self.student.last_name


class Checked(models.Model):
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.student_class.class_name
    


