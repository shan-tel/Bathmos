from django.shortcuts import render

def home(request):
    return render(request, 'talmidin/index.html')

def login_select(request):
    return render (request, 'talmidin/login_select.html')

def teacher_login(request):
    return render(request, 'talmidin/teacher_login.html')

def student_login(request):
    return render(request, 'talmidin/student_login.html')