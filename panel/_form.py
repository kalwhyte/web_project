from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Student, Teacher, Admin, Subject
from django.db import models




GENDER = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
]
class AdminRegistrationForm(UserCreationForm):
    """
    adding extra field to the User created form
    to create a User named Admin
    admin registration form 
    """
    phone_number = forms.CharField(max_length=11)
    email = forms.EmailField()
    address = forms.CharField(max_length=50)


class TeacherRegistrationForm(UserCreationForm):
    """
    Teacher registration form fields
    """
    phone_number = forms.CharField(max_length=11)
    email = forms.EmailField()
    address = forms.CharField(max_length=50)
    

class StudentRegistrationForm(UserCreationForm):
    """
    Student registration form fields
    """
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female')])
    class Meta:
        model = Student
        fields = UserCreationForm.Meta.fields + ('phone_number', 'address', 'subjects', 'dob', 'std_class', 'email', 'gender')
    
    def save(self, commit=True):
        user = super().save(commit=False)

        # Retrieves the cleaned data from the form
        #username = self.cleaned_data['username']
        phone_number = self.cleaned_data['phone_number']
        address = self.cleaned_data['address']
        std_class = self.cleaned_data['std_class']
        dob = self.cleaned_data['dob']
        email = self.cleaned_data['email']
        gender = self.cleaned_data['gender']

        # Assigns the cleaned data to the user object
        if commit:
            #user.username = username
            user.save()

            # Creates a student object with the user object
            student = Student.objects.create(
                user=user,
                phone_number=phone_number,
                address=address,
                dob=dob,
                std_class=std_class,
                email=email,
                gender=gender,
            )

            # If the student is in JSS 1, 2 or 3, add all subjects to the student
            # if std_class is not None:
            #     default_subjects = Subject.objects.filter(name__lte=8)
            #     student.subjects.add(*default_subjects)
        return user
        
    # def clean(self):
    #     cleaned_data = super().clean()
    #     std_class = cleaned_data.get("std_class")
    #     if std_class and 'subjects' in self.cleaned_data:
    #         del self.cleaned_data['subjects']
    #     return cleaned_data

