from django.shortcuts import render, redirect

from school_website.forms import UserForm
from school_website import models


class Teacher:
    @staticmethod
    def add(request):
        if request.method == 'GET':
            form = UserForm()
            return render(request, 'add_teacher.html', context={'form': form})
        else:
            form = UserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                teacher = models.Teacher.objects.create(user=user)
            #     mesaj qoy bitch

            return redirect('home')




        #     username = request.POST.get('username', '')
        #     password = request.POST.get('password', '')
        #     user = authenticate(username=username, password=password)
        #     if user is not None:
        #         login(request, user)
        # return render(request, 'add_teacher.html', context={
        #     'error': 'İstifadəçı adı və ya şifrə yanlışdır'
        # })
