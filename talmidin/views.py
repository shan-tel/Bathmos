from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.http import HttpResponse
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from .models import ClassName, Student, Subject, Score, Teacher
from django.contrib.auth.models import User

def home(request):
    return render(request, 'talmidin/index.html')

def login_select(request):
    return render (request, 'talmidin/login_select.html')

def teacher_login(request):
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            try:
                teacher = Teacher.objects.get(user=user)
                login(request, user)
                return redirect('/teacher_login_select/')
            except Teacher.DoesNotExist:
                error = "This account is not a teacher account."
        else:
            error = "Wrong username or password."
    return render(request, 'talmidin/teacher_login.html', {'error': error})

def student_login(request):
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            try:
                student = Student.objects.get(user=user)
                login(request, user)
                return redirect('/student_scoresheet/')
            except Student.DoesNotExist:
                error = "This account is not a student account."
        else:
            error = "Wrong username or password."
    return render(request, 'talmidin/student_login.html', {'error': error})

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

        if not (ca1_value and ca2_value and test_value and exam_value):
            continue

        if float(ca1_value) > 10 or float(ca2_value) > 10 or float(test_value) > 20 or float(exam_value) > 60:
            continue

        Score.objects.update_or_create(
            student=student,
            subject=subject_obj,
            defaults={
                'CA1': ca1_value,
                'CA2': ca2_value,
                'TEST': test_value,
                'EXAMS': exam_value,
            }
        )

    messages.success(request, f"Scores saved for {subject_obj.name} - {class_obj.name}")
    return redirect('/teacher_login_select/')
def student_scoresheet(request):
    student = Student.objects.get(user=request.user)
    scores = Score.objects.filter(student=student)

    score_data = []
    for score in scores:
        classmates_scores = Score.objects.filter(
            subject=score.subject,
            student__class_name=student.class_name
        )
        highest = max(classmates_scores, key=lambda s: s.total())
        lowest = min(classmates_scores, key=lambda s: s.total())

        score_data.append({
            'subject': score.subject.name,
            'ca1': score.CA1,
            'ca2': score.CA2,
            'test': score.TEST,
            'exam': score.EXAMS,
            'total': score.total(),
            'grade': score.grade(),
            'highest': highest.total(),
            'lowest': lowest.total(),
        })

    return render(request, 'talmidin/student_scoresheet.html', {
        'student': student,
        'score_data': score_data,
    })


GRADE_REMARKS = {
    'A': 'Excellent',
    'B': 'Very Good',
    'C': 'Good',
    'D': 'Fair',
    'E': 'Poor',
    'F': 'Fail',
}



def student_scoresheet_pdf(request):
    student = Student.objects.get(user=request.user)
    scores = Score.objects.filter(student=student)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="scoresheet.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    p.setTitle(f"{student.name} - Scoresheet")
    width, height = A4

    p.setFont("Helvetica-Bold", 18)
    p.setFillColorRGB(0.65, 0.16, 0.16)
    p.drawString(50, height - 50, "Bathmos Nursery and Primary School")

    if student.passport:
        p.drawImage(student.passport.path, width - 150, height - 150, width=100, height=100)

    p.setFont("Helvetica", 12)
    p.setFillColorRGB(0, 0, 0)
    p.drawString(50, height - 90, f"Name: {student.name}")
    p.drawString(50, height - 110, f"Date of Birth: {student.date_of_birth}")
    p.drawString(50, height - 130, f"Class: {student.class_name.name}")

    # Build table data: header row first, then one row per subject
    table_data = [["Subject", "CA1", "CA2", "Test", "Exam", "Total", "Grade", "Highest", "Lowest", "Remark"]]

    for score in scores:
        classmates_scores = Score.objects.filter(
            subject=score.subject,
            student__class_name=student.class_name
        )
        highest = max(classmates_scores, key=lambda s: s.total())
        lowest = min(classmates_scores, key=lambda s: s.total())
        grade = score.grade()
        remark = GRADE_REMARKS.get(grade, '')

        table_data.append([
            score.subject.name, str(score.CA1), str(score.CA2),
            str(score.TEST), str(score.EXAMS), str(score.total()),
            grade, str(highest.total()), str(lowest.total()), remark
        ])

    table = Table(table_data, colWidths=[70, 30, 30, 30, 30, 35, 35, 30, 30, 60])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.65, 0.16, 0.16)),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.Color(0.97, 0.95, 0.93)]),
    ]))

    table_width, table_height = table.wrap(0, 0)
    table.drawOn(p, 50, height - 180 - table_height)

    y = height - 200 - table_height
    p.setFont("Helvetica", 11)
    p.drawString(50, y, "Remark: _______________________________")
    y -= 30
    p.drawString(50, y, "Teacher's Signature: ___________________")

    p.showPage()
    p.save()

    return response

def logout_view(request):
    logout(request)
    return redirect('/')

# def setup_admin(request):
#     if User.objects.filter(username='admin').exists():
#         return HttpResponse("Admin already exists.")
#
#     User.objects.create_superuser(
#         username='admin',
#         password='BathmosAdmin123!',
#         email='admin@bathmos.com'
#     )
#
#     return HttpResponse("Admin created successfully.")

def setup_admin(request):
    from django.contrib.auth.models import User
    from django.http import HttpResponse

    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@bathmos.com', 'admin123')
        return HttpResponse("Omo, Admin created! Username is 'admin' and Password is 'admin123'")

    return HttpResponse("Admin already exists.")