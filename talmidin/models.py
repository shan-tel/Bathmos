from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ClassName(models.Model):
    name = models.CharField(max_length=100)
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    student_id = models.CharField(max_length=100)
    passport = models.ImageField(upload_to='passports')
    class_name = models.ForeignKey(ClassName, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Score(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    CA1 = models.DecimalField(max_digits=4, decimal_places=2)
    CA2 = models.DecimalField(max_digits=4, decimal_places=2)
    TEST = models.DecimalField(max_digits=4, decimal_places=2)
    EXAMS = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.student} - {self.subject}"

    def total(self):
        sum = self.CA1 + self.CA2 + self.TEST + self.EXAMS
        return sum


    def grade(self):
        if self.total()>=70:
            return "A"
        elif self.total()>=60:
            return "B"
        elif self.total()>=50:
            return "C"
        elif self.total()>=40:
            return "D"
        elif self.total()>=30:
            return "E"
        else:
            return "F"
