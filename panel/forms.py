from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Student, Teacher, Admin, Subject, StdClass,Session,SubjectScore
from django.contrib.auth.models import User
from django.db import models
from django.forms import BaseFormSet


GENDER = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
]
class SessionCreationForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = "__all__"

class AdminRegistrationForm(UserCreationForm):
    """
    adding extra field to the User created form
    to create a User named Admin
    admin registration form 
    """
    phone_number = forms.CharField(max_length=11)
    #email = forms.EmailField()
    address = forms.CharField(max_length=50)


class TeacherRegistrationForm(UserCreationForm):
    """
    Teacher registration form fields
    """
    phone_number = forms.CharField(max_length=20)
    email = forms.EmailField()
    address = forms.CharField(max_length=50)
    gender =forms.ChoiceField(choices=GENDER)
    



class StudentRegistrationForm(forms.ModelForm):
    """
    Student registration form fields
    """
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    phone_number = forms.CharField(max_length=20)
    email = forms.EmailField()
    address = forms.CharField(max_length=50)
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    std_class = forms.ModelChoiceField(queryset=StdClass.objects.all())
    gender = forms.ChoiceField(choices=GENDER)
    session = forms.ModelChoiceField(queryset=Session.objects.all())

    class Meta:
        model = Student
        fields = ['username', 'password', 'phone_number', 'email', 'address', 'dob', 'std_class', 'gender',]

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        student = super().save(commit=False)
        student.role = "student"
        student.user = user
        if commit:
            student.save()
        return student
    

class StudentUpdateForm(forms.ModelForm):
    """
    Student update form fields"""
    class Meta:
        model = Student
        exclude = ['user','role']
        

class UserUpdateForm(forms.ModelForm):
    """
    updating the user instance"""
    class Meta:
        model = User
        fields = ['username']

class ClassRegistrationForm(forms.ModelForm):
    """
    Class registration form fields
    """
    class Meta:
        model = StdClass
        fields = '__all__'

class SubjectRegistrationForm(forms.ModelForm):
    """
    Subject registration form fields
    """
    class Meta:
        model = Subject
        fields = '__all__'

class TeacherUpdateForm(forms.ModelForm):
    """
    Teacher update form fields
    """
    class Meta:
        model = Teacher
        exclude = ['user','role']


class AdminUpdateForm(forms.ModelForm):
    """
    Admin update form fields
    """
    class Meta:
        model = Admin
        exclude = ['user','role']


class BaseSubjectScoreFormSet(BaseFormSet):
    def clean(self):
        for form in self.forms:
            score = form.cleaned_data.get('score')
            if score is not None and (score < 0 or score > 100):
                raise forms.ValidationError('Score must be between 0 and 100')


class SubjectScoreUpdateForm(forms.ModelForm):
    """
    class to score students
    """
    class  Meta:
        model = SubjectScore
        fields = ['score']
        #fields = "__all__"