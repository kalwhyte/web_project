"""
modules containing the database structure of the codetrybe webapp
"""
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
GENDER = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
]

class Session(models.Model):
    """
    a model for sessions table
    """
    Year = models.CharField(max_length=50)
    Term = models.CharField(max_length=50,default=None)

    def __str__(self):
        return self.Year
    

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20,default="0802")
    address = models.CharField(max_length=50,default="Default address")
    role = models.CharField(max_length=20,default="admin") 

    def __str__(self):
        return self.user.username


class Teacher(models.Model):
    """
    a model for Teachers table
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20,default="+234-")
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=50,default="Default address")
    gender = models.CharField(max_length=40,default="male")
    role = models.CharField(max_length=20,default="teacher") 

    def __str__(self):
        return self.user.username


class Subject(models.Model):
    """
    subjects offered by students
    """
    name = models.CharField(max_length=30)
    Teacher = models.ManyToManyField(Teacher,related_name="subject_taught")

    def __str__(self):
        return self.name


# need to thing 


class StdClass(models.Model):
    """
    all classes in the school
    """
    name = models.CharField(max_length=40)
    subject = models.ManyToManyField(Subject,related_name="classes")
    class_teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    session = models.ForeignKey(Session, on_delete=models.CASCADE,default=None)

    def get_students(self):
        students = Student.objects.filter(std_class=self)
        return students
    
    
    def __str__(self):
        return self.name     


class Student(models.Model):
    """
    a model for Student table
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20,default="+234-")
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=50,default="Default address")
    dob = models.DateField(null=True,blank=True)
    std_class = models.ForeignKey(StdClass, on_delete=models.CASCADE, default=None)
    gender = models.CharField(max_length=10, default='NULL')
    role = models.CharField(max_length=20,default="student") 

    def __str__(self):
        return self.user.username

    @classmethod
    def get_students(cls):
        students = cls.objects.all()
        return students


class SubjectScore(models.Model):
    """
    a model for Subject Score
    """
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    score = models.IntegerField(null=True, blank=True) 

    def __str__(self):
        return f"{self.student.user.username} {self.subject.name}"
    
