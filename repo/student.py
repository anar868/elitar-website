from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect

from school_website import models
from school_website.forms import StudentForm, UserForm, RegistrationForm
from school_website.models import Class, Student, MissingStudents, Checked
import datetime


class StudentClass:
    @staticmethod
    def add(request):
        if request.method == 'GET':
            form1 = UserForm()
            form2 = StudentForm()
            return render(request, 'add_student.html', context={'form1': form1, 'form2': form2})
        else:
            form1 = UserForm(request.POST)
            form2 = StudentForm(request.POST)
            if form1.is_valid() and form2.is_valid():
                user = form1.save(commit=False)
                user.save()
                student_class_id = request.POST.get('student_class')
                student_class_2 = Class.objects.get(id=student_class_id)
                student = models.Student.objects.create(user=user, student_class=student_class_2)
                return render(request, 'add_student.html', context={'user_name': user.first_name + " " + user.last_name,
                                                                    'form1': form1, 'form2': form2})
            else:
                return render(request, 'add_student.html', context={'form1': form1, 'form2': form2})

            #     mesaj qoy bitch

    @staticmethod
    def add_missing(request):
        if request.user.is_superuser:
            return redirect('class_list')
        if request.user.is_authenticated:
 
            student_class = request.user.student_class
            
            checked_class = 'no'

            for classes in Checked.objects.all():
                if classes.datetime.date() == datetime.datetime.today().date() and classes.student_class == student_class:
                    checked_class = 'yes'
                else:
                    checked_class = 'no'

            missing_student_ids = []
            missing_students = []
            for student in MissingStudents.objects.order_by('student__first_name'):
                if student.datetime.date() == datetime.datetime.today().date() and student.student.student_class == student_class:
                    missing_student_ids.append(student.student.id)
                    missing_students.append(student)
            students = Student.objects.filter(student_class=student_class).exclude(id__in=missing_student_ids).order_by('first_name')
            student_count = len(students)
            missing_count = len(missing_students)
            return render(request, 'add_missing.html', context={'students': students,
                                                                'student_count': student_count,
                                                                'page': 'add_missing',
                                                                'missing_students': missing_students,
                                                                'missing_count': missing_count,
                                                                'student_class': student_class,
                                                                'checked_class': checked_class,
                                                                })
        else:
            return redirect('login')

    @staticmethod
    def user_login(request):
        if not request.user.is_authenticated:
            if request.method == 'GET':
                return render(request, 'login.html', context={'page': 'login'})
            else:
                username = request.POST.get('username', '')
                password = request.POST.get('password', '')
                if not username or not password:
                    return render(request, 'login.html', context={'error_message': 'Invalid',
                                                                'username': username,
                                                                'password': password,
                                                                'page': 'login'
                                                                })
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('add_missing')
                else:
                    return render(request, 'login.html', context={'error_message': 'Invalid',
                                                                  'username': username,
                                                                  'password': password,
                                                                  'page': 'login'
                                                                  })
        return redirect('home')

    @staticmethod
    def user_logout(request):
        logout(request)
        return redirect('home')


    @staticmethod
    def remove_missing(request):
        if request.method != 'GET':
            if request.POST.get('remove_missing') == 'remove_missing':
                missing_student_id = request.POST.get('missing_student_id')
                missing_student_first_name = request.POST.get('missing_student_first_name')
                if MissingStudents.objects.get(id=missing_student_id).student.first_name == missing_student_first_name:
                    MissingStudents.objects.get(id=missing_student_id).delete()
            if request.POST.get('add_missing') == 'add_missing':
                student_id = request.POST.get('student_id')
                student_first_name = request.POST.get('student_first_name')
                if Student.objects.get(id=student_id).first_name == student_first_name:
                    MissingStudents.objects.create(student=Student.objects.get(id=student_id))
        return redirect('add_missing')


    @staticmethod
    def class_checked(request):
        if request.method != 'GET':
            if request.POST.get('check_class') == 'check_class':
                class_id = request.POST.get('class_id')
                class_name = request.POST.get('class_name')
                if Class.objects.get(id=class_id).class_name == class_name:
                    Checked.objects.create(student_class=Class.objects.get(id=class_id))
        return redirect('add_missing')


    @staticmethod
    def class_list(request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                classes = Class.objects.order_by('-grade_number', '-class_name')
                missing_students_count = {}
                students_count = {}

                for student_class in classes:
                    missing_students_count[student_class] = len(MissingStudents.objects.filter(datetime__gt=datetime.date.today(), student__student_class=student_class))
                    students_count[student_class] = len(Student.objects.filter(student_class=student_class)) - missing_students_count[student_class]
                checked_classes = []

                for checked in Checked.objects.all():
                    if checked.datetime.date() == datetime.datetime.today().date():
                        checked_classes.append(checked.student_class)

                return render(request, 'classes_list.html', context={
                    'checked_classes': checked_classes,
                    'classes': classes,
                    'missing_students_count': missing_students_count,
                    'students_count': students_count
                })
                        
                
        else:
            redirect('add_missing')
    
    @staticmethod
    def missing_students(request, class_id):
        if not request.user.is_superuser:
            return redirect('add_missing')
        if request.user.is_authenticated:

            student_class = Class.objects.get(id=class_id)

            missing_student_ids = []
            missing_students = []
            for student in MissingStudents.objects.order_by('student__first_name'):
                if student.datetime.date() == datetime.datetime.today().date() and student.student.student_class == student_class:
                    missing_student_ids.append(student.student.id)
                    missing_students.append(student)
            students = Student.objects.filter(student_class=student_class).exclude(id__in=missing_student_ids).order_by('first_name')
            student_count = len(students)
            missing_count = len(missing_students)
            date_of_today = datetime.datetime.today().date()
            return render(request, 'missing_students.html', context={'students': students,
                                                                'student_count': student_count,
                                                                'page': 'add_missing',
                                                                'missing_students': missing_students,
                                                                'missing_count': missing_count,
                                                                'student_class': student_class,
                                                                'date_of_today': date_of_today
                                                                })
        else:
            return redirect('login')
        
    @staticmethod
    def add_user(request):
        if request.user.is_authenticated and request.user.username == 'anar2005':
            if request.method == 'GET':
                form = RegistrationForm(request.POST)
                student_classes = Class.objects.all()
                return render(request, 'add_user.html', context={'form': form, 'student_classes': student_classes})
            else:
                form = RegistrationForm(request.POST)
                if form.is_valid():
                    user = form.save(commit=False)
                    user.author = request.user
                    user.save()
                    return redirect('add_missing')
            return redirect('add_user')
        return redirect('logout')