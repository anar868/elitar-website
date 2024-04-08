from django.shortcuts import render

from school_website.forms import ClassForm


class Class:
    @staticmethod
    def add(request):
        if request.method == 'GET':
            form = ClassForm()
            return render(request, 'add_class.html', context={'form': form})
        else:
            form = ClassForm(request.POST)
            if form.is_valid():
                student_class = form.save(commit=False)
                student_class.save()
            #     mesaj qoy bitch

            return render(request, 'add_class.html', context={'form': form})

    def add_missing(request):
        return render(request, 'add_missing.html')
