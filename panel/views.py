from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Admin, Teacher, Student, Subject,StdClass,Session,SubjectScore
from .forms import (AdminRegistrationForm, TeacherRegistrationForm, 
StudentRegistrationForm, ClassRegistrationForm, SubjectRegistrationForm,SessionCreationForm,
SubjectScoreUpdateForm,
StudentUpdateForm, UserUpdateForm, TeacherUpdateForm, AdminUpdateForm)
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.db.models import Case, When, Value, IntegerField


# Create your views here.
def home(request):
    return render(request, template_name="panel/index.html")


#@login_required
def welcome(request):
    return render(request, template_name="panel/index.html")


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            try:
                user = User.objects.get(username=username)
                if user.check_password(password):
                    authenticated_user = authenticate(username=username, password=password)
                    login(request, authenticated_user)

                    # if user is admin
                    try:
                        Admin.objects.get(user=user)
                        return redirect("panel-adminpage")
                        # return render(request, 'panel/admin.html', {"admin_instance": admin_instance})
                    except Admin.DoesNotExist:
                        pass

                    try:
                        Teacher.objects.get(user=user)
                        return redirect("panel-teachpage")
                    except Teacher.DoesNotExist:
                        pass

                    try:
                        Student.objects.get(user=user)
                        return redirect("panel-studentpage")
                    except Student.DoesNotExist:
                        pass
                    

                else:
                    # Return an 'invalid login' error message.
                    form.add_error('password', 'Invalid username or password')
            except User.DoesNotExist:
                form.add_error('username', 'Invalid username or password')
    else:
        form = AuthenticationForm()

    return render(request,'panel/login.html',{'form':form})


@login_required
def student(request):
    user = request.user
    student_instance = Student.objects.get(user=user)
    return render(request, 'panel/student.html',{'student_instance':student_instance})

@login_required
def admin(request):
    user = request.user
    admin_instance = Admin.objects.get(user=user)
    return render(request, 'panel/admin.html',{'admin_instance':admin_instance})



@login_required
def teacher(request):
    user = request.user
    teacher_instance = Teacher.objects.get(user=user)
    return render(request, 'panel/teach.html',{'teacher_instance':teacher_instance})





@login_required
def StdReg(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            
            try:
                password = form.cleaned_data['password']
                confirm_password = form.cleaned_data['confirm_password']
                if password!= confirm_password:
                    messages.error(request,"unmatching password")
                    return render(request, "panel/StdReg.html", {'form':form})
                username = form.cleaned_data['username']
                try:
                    data = User.objects.get(username=username)
                    messages.error(request, "Username already exists")
                    return render(request, "panel/StdReg.html", {'form': form})
                except User.DoesNotExist:
                    pass
                user = form.save(commit=False)
                phone_number=form.cleaned_data['phone_number']
                email=form.cleaned_data['email']
                address=form.cleaned_data['address']
                dob=form.cleaned_data['dob']
                gender=form.cleaned_data['gender']
                user.save()
                student =  Student.objects.create(
                    user=user,
                    phone_number=phone_number,
                    email=email,
                    address=address,
                    dob=dob,
                    gender=gender
                )
            except ValueError:
            # Silencing the ValueError
                pass
            except Exception as e:
            # Handle other exceptions
                 raise e
                # Redirect to the home page
            messages.success(request,"student successfully created")
            return render(request, "panel/admin.html") 
    # If the request is a GET request, create an empty form instance and render it    
    form = StudentRegistrationForm()
    return render(request, "panel/StdReg.html", {'form': form, 'messages': messages.get_messages(request)})
    

@login_required
def admReg(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            form.instance.role = "admin"
            user = form.save()
            phone_number=form.cleaned_data['phone_number']
            #email=form.cleaned_data['email']
            address=form.cleaned_data['address']

            Admin.objects.create(user=user, phone_number=phone_number, address=address)
            messages.success(request,'Admin Successfully Created')
            return redirect('panel-admRegpage')
        else:
            messages.error(request,f"refused to create {form.errors}")
    form = AdminRegistrationForm()
    return render(request, "panel/admReg.html", {'form':form})


@login_required
def tchReg(request):
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            form.instance.role = "teacher"
            user = form.save()
            Teacher.objects.create(user=user, phone_number=form.cleaned_data['phone_number'])
            return render(request, 'panel/admin.html')
        else:
            messages.error(request,f"refused to create {form.errors}")
            
    form = TeacherRegistrationForm()
    return render(request, "panel/tchReg.html", {'form':form})


@login_required
def clsReg(request):
    if request.method == 'POST':
        form = ClassRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Class Successfully Created')
            return render(request, 'panel/admin.html')
    form = ClassRegistrationForm()
    return render(request, "panel/clsReg.html", {'form':form,'tag':'class'})


@login_required
def sectionReg(request):
    if request.method == 'POST':
        form = SessionCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Section Successfully Created')
            return render(request, 'panel/admin.html')
    form = SessionCreationForm()
    return render(request, "panel/clsReg.html", {'form':form,'tag':'Section'})

@login_required
def subReg(request):
    if request.method == 'POST':
        form = SubjectRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Subject Successfully Created')
            return render(request, 'panel/admin.html')
    form = SubjectRegistrationForm()
    return render(request, "panel/clsReg.html", {'form':form,'tag':'Subject'})
    

def about_page(request):
    return render(request, template_name="panel/about.html")


def Logout_view(request):
    logout(request)
    return render(request, 'panel/index.html')


@login_required
def all_student(request):
    student_list = Student.objects.all()
    return render(request, 'panel/all_student.html', {'student_list': student_list})

@login_required
def all_teachers(request):
    teacher_list = Teacher.objects.all()
    return render(request, 'panel/all_teachers.html', {'teacher_list': teacher_list})


@login_required
def all_admin(request):
    admin_list = Admin.objects.all()
    return render(request,'panel/all_admin.html', {'admin_list': admin_list})


@login_required
def all_class(request):
    class_list = StdClass.objects.all()
    return render(request, 'panel/all_class.html', {'class_list': class_list})


@login_required
def all_subject(request):
    subject_list = Subject.objects.all()
    return render(request, 'panel/all_subject.html', {'subject_list': subject_list})


@login_required
def all_section(request):
    section_list = Session.objects.all()
    return render(request,'panel/all_section.html',{'section_list':section_list})


@login_required
def std_update(request, id):
    student_instance = get_object_or_404(Student, id=id) 
    user_instance = get_object_or_404(User, username=student_instance.user)
    form = StudentUpdateForm(instance=student_instance)
    username_form = UserUpdateForm(instance=user_instance)

    if request.method == 'POST':
        form = StudentUpdateForm(request.POST, instance=student_instance)
        username_form = UserUpdateForm(request.POST, instance=user_instance)

        if form.is_valid() and username_form.is_valid():
            username_form.save()
            form.save()
            messages.success(request, "Student successfully updated")
            return render(request, "panel/admin.html")
        else:
            messages.error(request, f"Failed to update student {form.errors} ")


    context = {
        'form': form,
        'username_form': username_form,
    }
    form = StudentUpdateForm(instance=student_instance)
    username_form = UserUpdateForm(instance=user_instance)

    return render(request, "panel/std_up.html", context)


@login_required
def sub_update(request,id):
    subject_instance = get_object_or_404(Subject, id=id) 
    form = SubjectRegistrationForm(instance=subject_instance)
    if request.method == 'POST':
        form = SubjectRegistrationForm(request.POST,instance=subject_instance)
        if form.is_valid():
           
            form.save()
            messages.success(request, "Subject successfully updated")
            return redirect('panel-adminpage')
    
        return render(request, 'panel/all_up.html' ,{'form':form})
    return render(request, 'panel/all_up.html' ,{'form':form})


@login_required
def cls_update(request,id):
    std_class_instance = get_object_or_404(StdClass, id=id) 
    form = ClassRegistrationForm(instance=std_class_instance)
    if request.method == 'POST':
        form = ClassRegistrationForm(request.POST,instance=std_class_instance)
        if form.is_valid():
           
            form.save()
            messages.success(request, "Class successfully updated")
            return redirect('panel-adminpage')
    
        return render(request, 'panel/all_up.html',{'form':form})
    return render(request, 'panel/all_up.html',{'form':form})


@login_required
def tch_update(request, id):
    teacher_instance = get_object_or_404(Teacher, id=id)
    user_instance = get_object_or_404(User, username=teacher_instance.user)
    form = TeacherUpdateForm(instance=teacher_instance)
    username_form = UserUpdateForm(instance=user_instance)

    
    if request.method == 'POST':
        form = TeacherUpdateForm(request.POST,instance=teacher_instance)
        username_form = UserUpdateForm(request.POST, instance=user_instance)

        if form.is_valid() and username_form.is_valid():
            username_form.save()
            form.save()
            messages.success(request, "Teacher successfully updated")
            return render(request, 'panel/admin.html')
        else:
            messages.error(request, f"Failed to update teacher {form.errors} ")
    

    context = {
        'form': form,
        'username_form': username_form,
    }
    form = TeacherUpdateForm(instance=teacher_instance)
    username_form = UserUpdateForm(instance=user_instance)

    return render(request, "panel/tch_up.html", context)


@login_required
def adm_update(request,id):
    admin_instance = get_object_or_404(Admin, id=id)
    user_instance = get_object_or_404(User, username=admin_instance.user)
    form = AdminUpdateForm(instance=admin_instance)
    username_form = UserUpdateForm(instance=user_instance)

    
    if request.method == 'POST':
        form = AdminUpdateForm(request.POST,instance=admin_instance)
        username_form = UserUpdateForm(request.POST, instance=user_instance)

        if form.is_valid() and username_form.is_valid():
            username_form.save()
            form.save()
            messages.success(request, "Admin successfully updated")
            return redirect('panel-adminpage')
        else:
            messages.error(request, f"Failed to update admin {form.errors} ")
    
    context = {
        'form': form,
        'username_form': username_form,
        'instance': admin_instance,
    }
    form = AdminUpdateForm(instance=admin_instance)
    username_form = UserUpdateForm(instance=user_instance)

    return render(request, "panel/adm_up.html", context)


@login_required
def sec_update(request,id):
    section_instance = get_object_or_404(Session, id=id) 
    form = SessionCreationForm(instance=section_instance)
    if request.method == 'POST':
        form = SessionCreationForm(request.POST,instance=section_instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Section successfully updated")
            return redirect('panel-adminpage')
    
        return render(request, 'panel/all_up.html',{'form':form})
    return render(request, 'panel/all_up.html',{'form':form})



@login_required
def std_delete(request,pk):
    try:
        student_instance = get_object_or_404(Student, id=pk) 
        user_instance = get_object_or_404(User, username=student_instance.user.username)
    except Student.DoesNotExist:
        messages.error(request, "Student does not exist")
        return redirect('panel-adminpage')
    if request.method == 'POST':
        user_instance.delete()
        messages.success(request, "successfully deleted")
        return redirect('panel-adminpage')


@login_required
def adm_delete(request,pk):
    try:
        admin_instance = get_object_or_404(Admin, id=pk) 
        user_instance = get_object_or_404(User, username=admin_instance.user.username)
    except Admin.DoesNotExist:
        messages.error(request, "Admin does not exist")
        return redirect('panel-adminpage')
    if request.method == 'POST':
        user_instance.delete()
        messages.success(request, "successfully deleted")
        return redirect('panel-adminpage')


@login_required
def tch_delete(request,pk):
    try:
        teacher_instance = get_object_or_404(Teacher, id=pk) 
        user_instance = get_object_or_404(User, username=teacher_instance.user.username)
    except Teacher.DoesNotExist:
        messages.error(request, "Teacher does not exist")
        return redirect('panel-adminpage')
    if request.method == 'POST':
        user_instance.delete()
        messages.success(request, "successfully deleted")
        return redirect('panel-adminpage')


@login_required
def view_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    context = {'teacher': teacher}
    return render(request, 'panel/view_teacher.html', context)


@login_required
def cls_delete(request,pk):
    try:
        class_instance = get_object_or_404(StdClass, id=pk) 
    except StdClass.DoesNotExist:
        messages.error(request, "Class does not exist")
        return redirect('panel-adminpage')
    if request.method == 'POST':
        class_instance.delete()
        messages.success(request, "successfully deleted")
        return redirect('panel-adminpage')
    

@login_required
def sub_delete(request,pk):
    try:
        subject_instance = get_object_or_404(Subject, id=pk) 
    except Subject.DoesNotExist:
        messages.error(request, "Subject does not exist")
        return redirect('panel-adminpage')
    if request.method == 'POST':
        subject_instance.delete()
        messages.success(request, "successfully deleted")
        return redirect('panel-adminpage')
    

@login_required
def sec_delete(request,pk):
    try:
        section_instance = get_object_or_404(Session, id=pk) 
    except Session.DoesNotExist:
        messages.error(request, "Section does not exist")
        return redirect('panel-adminpage')
    if request.method == 'POST':
        section_instance.delete()
        messages.success(request, "successfully deleted")
        return redirect('panel-adminpage')

def contact(request):
    return render(request, template_name="panel/contact.html")


def privacy(request):
    return render(request, template_name="panel/privacy.html")


def view_teacher(request, id):
    user = get_object_or_404(Teacher, id=id)
    subjects = Subject.objects.filter(Teacher=user)
    context = {'user': user, 'subjects': subjects}
    return render(request, 'panel/v_tch.html', context)


def view_student(request, id):
    user = get_object_or_404(Student, id=id)
    stdClass = StdClass.objects.filter(name=user.std_class).first()
    class_subjects = stdClass.subject.all()
    class_session = stdClass.session
    context = {'user': user, 'stdClass': stdClass, 'class_subjects': class_subjects, 'class_session': class_session}
    return render(request, 'panel/v_std.html', context)


# def Score(request,cls,sub):
#     # if request.method == "POST":
#     mstd_class = StdClass.objects.filter(name=cls).first()
#     print(mstd_class)
#     students = Student.objects.filter(std_class = mstd_class)
#     subject = Subject.objects.get(name=sub)
#     form = SubjectScoreUpdateForm()
#     if request.method == "POST":
#         form = SubjectScoreUpdateForm(request.POST)
#         if form.is_valid():
#             form.save()
#     return render(request, 'panel/score.html',{"students":students,"subject":subject,"form":form})
"""
def Score(request, cls, sub):
    mstd_class = StdClass.objects.filter(name=cls).first()
    students = Student.objects.filter(std_class=mstd_class)
    subject = Subject.objects.get(name=sub)

    if request.method == "POST":
        form = SubjectScoreUpdateForm(request.POST)
        if form.is_valid():
            for student in students:
                score, created = SubjectScore.objects.get_or_create(student=student, subject=subject)
                score.score = form.cleaned_data.get(f"student_{student.id}")  # Get the score for the current student
                score.save()

            # Handle successful form submission (e.g., redirect)
            return redirect('success-url')

    # Get the existing scores for each student and populate the form
    initial_scores = {}
    for student in students:
        score, created = SubjectScore.objects.get_or_create(student=student, subject=subject)
        initial_scores[f"student_{student.id}"] = score.score

    form = SubjectScoreUpdateForm(initial=initial_scores)

    return render(request, 'panel/score.html', {"students": students, "subject": subject, "form": form})



def allScore(request):
    if request.method == "POST":
        cls = request.POST.get("classname")
        if cls =="":
            messages.error(request,"please input a class name")
            return render(request, 'panel/std_cls.html')
        Cls = StdClass.objects.filter(name=cls).first()
        all_Std_class =  Student.objects.filter(std_class=Cls)
        if all_Std_class:
            Std_subs = Cls.subject.all()
            return render(request, 'panel/std_cls.html', {"all_Std_class": all_Std_class,"Std_subs":Std_subs,"cls":cls})
        else:
            messages.error(request,"no class with the inputed name")
    return render(request, 'panel/std_cls.html')
"""

def Score(request, cls, sub):
    mstd_class = StdClass.objects.filter(name=cls).first()
    students = Student.objects.filter(std_class=mstd_class)
    subject = Subject.objects.get(name=sub)
    subject_name = subject.name

    if request.method == "POST":
        formset = SubjectScoreUpdateForm(request.POST)
        if formset.is_valid():
            for student in students:
                score, created = SubjectScore.objects.get_or_create(student=student, subject=subject)
                score.score = formset.cleaned_data.get(f"student_{student.id}")
                score.save()
            # Handle successful form submission
            messages.success(request, "Scores successfully updated")
            return redirect('success-url')
    else:
        initial_scores = []
        for student in students:
            for student in students:
                score = student.subjectscore_set.filter(subject=subject).first()
                if score:
                    initial_scores[f"student_{student.id}"] = score.score
            form = SubjectScoreUpdateForm(initial=initial_scores)

    return render(request, 'panel/score.html', {
        "students": students,
        "subject": subject,
        "subject_name": subject.name,
        "form": form,
    })


def allScore(request):
    if request.method == "POST":
        cls = request.POST.get("classname")
        if not cls:
            messages.error(request, "Please input a class name")
            return render(request, 'panel/std_cls.html')
        
        cls_obj = StdClass.objects.filter(name=cls).first()
        if not cls_obj:
            messages.error(request, "No class with the inputed name")
            return render(request, 'panel/std_cls.html')
    
        std_subs = cls_obj.subject.all()
        all_std_class = Student.objects.filter(std_class=cls_obj)

        return render(request, 'panel/std_cls.html', {"all_Std_class": all_std_class, "Std_subs": std_subs, "cls": cls})

    return render(request, 'panel/std_cls.html')
