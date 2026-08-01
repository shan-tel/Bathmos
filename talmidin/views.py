from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from .models import ClassName, Student, Subject

def home(request):
    return render(request, 'talmidin/index.html')

def login_select(request):
    return render (request, 'talmidin/login_select.html')

def teacher_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/teacher_login_select/')
        else:
            pass
    return render(request, 'talmidin/teacher_login.html')

def student_login(request):
    return render(request, 'talmidin/student_login.html')

def teacher_login_select(request):
    classes = ClassName.objects.all()
    return render(request, 'talmidin/teacher_login_select.html', {'classes': classes})

def subject_select(request):
    selected_class = request.POST['class_id']
    class_obj = ClassName.objects.get(id=selected_class)
    return render(request, 'talmidin/subject_select.html', {'class_obj': class_obj})

def score_entry(request):
    selected_class = request.POST['class_id']
    selected_subject = request.POST['subject_id']

    class_obj = ClassName.objects.get(id=selected_class)
    subject_obj = Subject.objects.get(id=selected_subject)

    students = Student.objects.filter(class_name=class_obj)

    return render(request, 'talmidin/score_entry.html', {
        'class_obj': class_obj,
        'subject_obj': subject_obj,
        'students': students,
    })


def save_scores(request):
    selected_class = request.POST['class_id']
    selected_subject = request.POST['subject_id']

    class_obj = ClassName.objects.get(id=selected_class)
    subject_obj = Subject.objects.get(id=selected_subject)

    students = Student.objects.filter(class_name=class_obj)

    for student in students:
        ca1_value = request.POST[f'ca1_{student.id}']
        ca2_value = request.POST[f'ca2_{student.id}']
        test_value = request.POST[f'test_{student.id}']
        exam_value = request.POST[f'exam_{student.id}']

        Score.objects.create(
            student=student,
            subject=subject_obj,
            CA1=ca1_value,
            CA2=ca2_value,
            TEST=test_value,
            EXAMS=exam_value,
        )

    return render(request, 'talmidin/score_success.html')