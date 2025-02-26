from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View
from .models import District
from .models import Batch
from .models import CourseChoices,TrainerName
from.utility import get_admission_number,get_password
from.models import students
from.forms import StudentRegisterForm
from django.db.models import Q
from authentication.models import Profile
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from authentication.permissions import permission_roles

class GetStudentObject:

    def get_student(self,request,uuid):

        try:
                        
            student = students.objects.get(uuid=uuid,)

            return student
        
        except:

            return redirect(request,'errorpages/error-404.html')
    
       
class Home(View):

    def get(self,request,*args,**kwargs):

        return render (request,'student/home.html' )
    

# @method_decorator(login_required(login_url = 'login'),name='dispatch')

# dispatch decides whether to go to get or post

# @method_decorator(permission_roles(roles=['Admin','Sales']),name='dispatch')

class DashboardView(View):

    def get(self,request,*args,**kwargs):

        return render (request,'student/dashboard.html' )

class StudentsListView(View):

    def get(self,request,*args,**kwargs):

        query = request.GET.get('query')

        if query:

            Students = students.objects.filter(Q(active_status =True)&(Q(first_name__icontains = query)|Q(second_name__icontains = query)|Q(contact_num__icontains=query)|Q(house_name__icontains=query)|Q(post_office__icontains=query)|Q(pincode__icontains=query)|Q(course__code__icontains=query)))

        # Students = students.objects.all()

        Students = students.objects.filter(active_status = True )

        data ={'students':Students,'query':query}

        return render (request,'student/student.html',context=data )
    
class RegistrationView(View):

    def get(self,request,*args,**kwargs):

        form = StudentRegisterForm()

        # data ={'districts':District,'courses':CourseChoices,'batches':Batch,'trainers':TrainerName,'forms': form}

        data = {'form': form}
        
        return render (request,'student/registration.html',context=data)
    
    def post(self,request,*args,**kwargs):

        form = StudentRegisterForm(request.POST,request.FILES)

        if form.is_valid():

            with transaction.atomic():

                student=form.save(commit=False)

                student.adm_number =get_admission_number()

                # return render(request,'student/student.html')

                username = student.email

                password = get_password()

                print(password)

                profile = Profile.objects.create_user(username=username,password=password,role ='Student')

                student.profile = profile

                student.save()

            return redirect('student')
        
        else:

            data = {'form': form}

            return render(request,'student/registration.html',context=data)

@method_decorator(permission_roles(roles=['Admin','Sales','Trainer','Academic councillor']),name='dispatch')
class StudentDetailView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        # student = get_object_or_404(students,pk = pk)

        student = GetStudentObject().get_student(request,uuid)


        data = {'student':student}

        return render(request,'student/student-detail.html',context=data)
    
# class Error404View(View):

#     def get(self,request,*args,**kwargs):

#         return render(request,'student/error-404.html')

@method_decorator(permission_roles(roles=['Admin','Sales']),name='dispatch')
    
class StudentDeleteView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        student = GetStudentObject().get_student(uuid,request)

        student.active_status = False

        student.save()
   
        # student.delete()

        return redirect('students-list')
    
@method_decorator(permission_roles(roles=['Admin','Sales']),name='dispatch')

class StudentUpdateView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        student = GetStudentObject().get_student(uuid,request)

        form = StudentRegisterForm(instance=student)

        data ={'form': form}

        return render(request,'student/student-update.html',context = data)
    
    def post(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        student = GetStudentObject().get_student(uuid,request)

        form = StudentRegisterForm(request.POST,request.FILES,instance=student)

        if form.is_valid():

            form.save()

            return redirect('students-list')
        
        else :

            data ={'form':form}

            return render(request,'student/student-update.html',context= data)

            
        



        


        
    
    
       



