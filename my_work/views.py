from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse_lazy
from django.views.generic import View,CreateView,TemplateView,UpdateView,DetailView,ListView,FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from my_work.models import *
from my_work.forms import *
from django.contrib.auth.views import LoginView
from django.utils.timezone import now
from datetime import datetime, timedelta, date
from django.utils import timezone
from django.contrib.auth import login,logout
import datetime
from datetime import datetime
from django.utils.decorators import method_decorator
from django.http import Http404, HttpResponse
from django.contrib.auth import get_user_model
CustomUser = get_user_model()


def signin_requerd(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        else:
            return fn(request,*args,**kwargs)
    return wrapper


 

@method_decorator(signin_requerd,name="dispatch")
class EmployeeReg(View):
    def get(self, request, *args, **kwargs):
        form = register()
        return render(request, "registration.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = register(request.POST)
        if form.is_valid():
            CustomUser.objects.create_user(**form.cleaned_data)
            return redirect("admin_home")
        else:
            return render(request, "registration.html", {"form": form})
    




@method_decorator(signin_requerd,name="dispatch")     
class AdminHome(View):
    def get(self, request, *args, **kwargs):
        current_date = now().date()
        data = Attendancedb.objects.filter( date=current_date)
        return render(request, "adminindex.html", {"data": data})
    


@method_decorator(signin_requerd,name="dispatch")     
class ExicutiveHome(View):
    def get(self, request, *args, **kwargs):
        current_date = now().date()
        user = request.user.id
        profile = StaffProfile.objects.filter(user_id = user)
        data = Attendancedb.objects.filter(user=request.user, date=current_date)  
        return render(request, "exicutiveindex.html", {"data": data,"profile":profile})

@method_decorator(signin_requerd,name="dispatch")     
class EmployeeHome(View):
    def get(self, request, *args, **kwargs):
        current_date = now().date()
        user = request.user.id
        profile = StaffProfile.objects.filter(user_id = user)
        data = Attendancedb.objects.filter(user=request.user, date=current_date)  
        return render(request, "index.html", {"data": data,"profile":profile})


class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = CustomAuthenticationForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        if self.request.user.is_staff :
            return redirect('admin_home')  
        elif user.user_type == 'staff':
            return redirect('emp_home')  
        elif user.user_type == 'exicutive':
            return redirect('ex_home')     
        else:
            return redirect(self.success_url)
    


class EXicutiveDefaultAttendanceView(View):
    def get(self, request):
        checkin = now() + timedelta(hours=5, minutes=30)
        today = now().date()
        attendance_exists = Attendancedb.objects.filter(user=request.user, date=today).exists()

        if not attendance_exists:
            attendance = Attendancedb(
                user=request.user,
                checkin=checkin,
                start=True
            )
            attendance.save()

        return redirect('ex_home')
    
class ExicutiveUpdateCheckoutView(View):
    def get(self, request):
        current_date = now().date()
        current_time = now()+ timedelta(hours=5, minutes=30)        
        attendance_entries = Attendancedb.objects.filter(user=request.user, date=current_date)       
        if attendance_entries.exists():
            for entry in attendance_entries:
                entry.checkout = current_time
                entry.end = True 
                entry.save()
        return redirect('ex_home')




class AddDefaultAttendanceView(View):
    def get(self, request):
        checkin = now() + timedelta(hours=5, minutes=30)
        today = now().date()
        attendance_exists = Attendancedb.objects.filter(user=request.user, date=today).exists()

        if not attendance_exists:
            attendance = Attendancedb(
                user=request.user,
                checkin=checkin,
                start=True
            )
            attendance.save()

        return redirect('emp_home')
    


class UpdateCheckoutView(View):
    def get(self, request):
        current_date = now().date()
        current_time = now()+ timedelta(hours=5, minutes=30)        
        attendance_entries = Attendancedb.objects.filter(user=request.user, date=current_date)       
        if attendance_entries.exists():
            for entry in attendance_entries:
                entry.checkout = current_time
                entry.end = True 
                entry.save()
        return redirect('emp_home')
    
@method_decorator(signin_requerd,name="dispatch")
class ExLeaveRequest(CreateView):
    template_name = 'LeaveRequest.html'
    form_class = LeaveForm
    model = LeaveUpdate
    success_url = reverse_lazy('ex_home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.training_id = id
        return super().form_valid(form)

@method_decorator(signin_requerd,name="dispatch")
class LeaveRequest(CreateView):
    template_name = 'LeaveRequest.html'
    form_class = LeaveForm
    model = LeaveUpdate
    success_url = reverse_lazy('emp_home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.training_id = id
        return super().form_valid(form)
@method_decorator(signin_requerd,name="dispatch")
class ExLeaveStatus(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        data = LeaveUpdate.objects.filter(user_id = user)
        return render(request, "ExLeaveStatus.html", {"data": data})  

@method_decorator(signin_requerd,name="dispatch")
class LeaveStatus(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        data = LeaveUpdate.objects.filter(user_id = user)
        return render(request, "LeaveStatus.html", {"data": data})


class Signout(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('lgn')
    


@method_decorator(signin_requerd,name="dispatch")
class ListHolidays(View):
    def get(self, request, *args, **kwargs):
        data = GeneralHolidays.objects.all()
        return render(request, "ListHolidays.html", {"data": data})
    
@method_decorator(signin_requerd,name="dispatch")
class MonthlyAttendanceView(View):
    def get(self, request):
        month = request.GET.get('month', datetime.now().month)
        year = request.GET.get('year', datetime.now().year)

        monthly_records = Attendancedb.objects.filter(date__year=year, date__month=month)

        user_id = request.GET.get('user_id')
        if user_id:
            monthly_records = monthly_records.filter(user_id=user_id)

        context = {
            'monthly_records': monthly_records,
            'selected_month': month,
            'selected_year': year,
        }
        return render(request, 'monthly_attendance.html', context)
    
@method_decorator(signin_requerd,name="dispatch")
class MonthlyStatementView(View):
    def get(self, request):
        month = int(request.GET.get('month', datetime.now().month))
        year = int(request.GET.get('year', datetime.now().year))
        users = CustomUser.objects.filter(is_superuser = False)
        user_statements = {}

        for user in users:
            monthly_records = Attendancedb.objects.filter(user=user, date__year=year, date__month=month)
            user_statements[user] = monthly_records

        context = {
            'user_statements': user_statements,
            'selected_month': month,
            'selected_year': year,
        }
        return render(request, 'monthly_statement.html', context)
    



class SingleMonthlyStatementView(View):
    def get(self, request,**kwargs):
        month = int(request.GET.get('month', datetime.now().month))
        year = int(request.GET.get('year', datetime.now().year))
        id = kwargs.get("pk")
        users = CustomUser.objects.filter(id = id)
        user_statements = {}

        for user in users:
            monthly_records = Attendancedb.objects.filter(user=user, date__year=year, date__month=month)
            user_statements[user] = monthly_records

        context = {
            'user_statements': user_statements,
            'selected_month': month,
            'selected_year': year,
        }
        return render(request, 'SingleMonthlyStatement.html', context)
    



class EmployeeList(View):
    def get(self, request, *args, **kwargs):
        data = CustomUser.objects.all()
        return render(request, "EmployeeList.html", {"data": data})
    

class MyAttendence(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        date = now().date()
        data = Attendancedb.objects.filter(date = date,user_id = user)
        return render(request, "MyAttendence.html", {"data": data})
    

class DutyOnprogress(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        date = now().date()
        data = Attendancedb.objects.filter(date = date,user_id = user)
        return render(request, "DutyOnprogress.html", {"data": data})
    



class EmployeeMonthlyAttendence(View):
    template_name = 'EmployeeMonthlyAttendence.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        month = request.GET.get('month', datetime.now().month)
        year = request.GET.get('year', datetime.now().year)
        

        try:
            month = int(month)
            year = int(year)
        except ValueError:
            month = datetime.now().month
            year = datetime.now().year

        attendance_data = Attendancedb.objects.filter(user=user, date__year=year, date__month=month)
        leaves = LeaveUpdate.objects.filter(user=user)

        context = {
            'attendance_data': attendance_data,
            'month': month,
            'year': year,
            'leaves':leaves
        }

        return render(request, self.template_name, context)
    



class MonthlyAttendanceList(View):
    form_class = MonthYearUserForm
    template_name = 'monthlyListattendance.html'
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            month = form.cleaned_data['month']
            user = form.cleaned_data['user']
            start_date = date(year, month, 1)
            if month == 12:
                end_date = date(year + 1, 1, 1) - timedelta(days=1)
            else:
                end_date = date(year, month + 1, 1) - timedelta(days=1)
            attendance_records = Attendancedb.objects.filter(date__range=(start_date, end_date))
            if user:
                attendance_records = attendance_records.filter(user=user)
            context = {
                'form': form,
                'attendance_records': attendance_records,
                'month': month,
                'year': year,
                'user': user,
            }
            return render(request, self.template_name, context)
        return render(request, self.template_name, {'form': form})
    




class ProfileCreation(CreateView):
    template_name = 'ProfileCreation.html'
    form_class = ProfileForm
    model = StaffProfile
    success_url = reverse_lazy('emp_home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.training_id = id
        return super().form_valid(form)   




class ProfileListView(View):
    def get(self,request,*args,**kwargs):
        user = request.user.id
        profile = StaffProfile.objects.filter(user_id = user)
        data = CustomUser.objects.get(id= user)
        return render(request,"ProfileListView.html",{"profile":profile,"data":data})
    




class GeneralLeaveView(CreateView):
    template_name = 'GeneralLeaveView.html'
    form_class = GeneralLeave
    model = GeneralHolidays
    success_url = reverse_lazy('admin_home')




class GeneralLeaveList(View):
    def get(self, request, *args, **kwargs):
        user = request.user.id
        data = CustomUser.objects.get(id=user)
        today = timezone.now().date()
        leave = GeneralHolidays.objects.filter(date__gte=today)
        
        if data.user_type == "exicutive":
            return render(request, "GeneralLeaveList.html", {"leave": leave})
        else:
            return render(request, "EmpGeneralLeaveList.html", {"leave": leave})


class DailyTaskUpdate(CreateView):
    template_name = 'TailyTaskUpdate.html'
    form_class = DailyTskForm
    model = DailyUpdateModel
    success_url = reverse_lazy('admin_home')




class DailyTaskList(View):
    def get(self, request, *args, **kwargs):
        user = request.user.id
        data = CustomUser.objects.get(id=user)
        today = timezone.now().date()
        task = DailyTaskModel.objects.filter(date__gte=today,user_id = user)
        
        if data.user_type == "exicutive":
            return render(request, "DailyTaskList.html", {"task": task})
        else:
            return render(request, "Emp_DailyTaskList.html", {"task": task})



    
class DailyExicutiveUpdate(CreateView):
    template_name = 'DailyExicutiveUpdate.html'
    form_class = UpdateForm
    model = DailyUpdateModel
    success_url = reverse_lazy('ex_home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.training_id = id
        return super().form_valid(form)   

    


class AllUpdates(View):
    def get(self,request,*args,**kwargs):
        updates = DailyUpdateModel.objects.all()
        return render(request,"AllUpdates.html",{"updates":updates})
    


class singleUpdates(View):
    def get(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        updates = DailyUpdateModel.objects.get(id=id)
        return render(request,"singleUpdates.html",{"updates":updates})





class RemarkUpdate(UpdateView):
    model = DailyUpdateModel
    form_class = RemarkUpdateForm
    template_name = 'update_form.html'
    success_url = reverse_lazy('admin_home')




class GetLeaveRequest(View):
    def get(self,request,*args,**kwargs):
        leave = LeaveUpdate.objects.filter(status = False)
        accepted = LeaveUpdate.objects.filter(status = True)
        return render(request,"GetLeaveRequest.html",{"leave":leave,"accepted":accepted})

     

class LeaveConFormation(View):
     def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=LeaveUpdate.objects.get(id=id)
        if qs.status == False:
            qs.status= True
            qs.save()
        return redirect("all_leave")
     



class AddExpence(CreateView):
    template_name = 'AddExpence.html'
    form_class = ExpenceForm
    model = ExpenceModel
    success_url = reverse_lazy('ex_home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.training_id = id
        return super().form_valid(form)



class PendingExpence(View):
    def get(self,request,*args,**kwargs):
        expenses = ExpenceModel.objects.filter(approve = False,reject = False)
        return render(request,"PendingExpence.html",{"expenses":expenses})


class AcceptedExpence(View):
    def get(self,request,*args,**kwargs):
        expenses = ExpenceModel.objects.filter(approve = True,reject = False)
        return render(request,"AcceptedExpence.html",{"expenses":expenses})
    
    

class RejectedExpence(View):
    def get(self,request,*args,**kwargs):
        expenses = ExpenceModel.objects.filter(approve = False,reject = True)
        return render(request,"RejectedExpence.html",{"expenses":expenses})
    
    
class AcceptExpence(View):
     def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=ExpenceModel.objects.get(id=id)
        if qs.approve == False:
            qs.approve = True
            qs.save()
        return redirect("pending_exp")
     

class RejectExpence(View):
     def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=ExpenceModel.objects.get(id=id)
        if qs.reject == False:
            qs.reject = True
            qs.save()
        return redirect("pending_exp")
     


class ExpenceView(View):
    def get(self,request,*args,**kwargs):
        user = request.user
        expenses = ExpenceModel.objects.filter(user = user)
        return render(request,"ExpenceView.html",{"expenses":expenses})
    



class MonthlyUpdateList(View):
    form_class = MonthYearUserForm
    template_name = 'MonthlyUpdateList.html'
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            month = form.cleaned_data['month']
            user = form.cleaned_data['user']
            start_date = date(year, month, 1)
            if month == 12:
                end_date = date(year + 1, 1, 1) - timedelta(days=1)
            else:
                end_date = date(year, month + 1, 1) - timedelta(days=1)
            records = DailyUpdateModel.objects.filter(date__range=(start_date, end_date))
            if user:
                records = records.filter(user=user)
            context = {
                'form': form,
                'records': records,
                'month': month,
                'year': year,
                'user': user,
            }
            return render(request, self.template_name, context)
        return render(request, self.template_name, {'form': form})





class WeeklyUpdateList(View):
    form_class = DateRangeUserForm
    template_name = 'WeeklyUpdateList.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            user = form.cleaned_data['user']
            records = DailyUpdateModel.objects.filter(date__range=(start_date, end_date))
            if user:
                records = records.filter(user=user)
            context = {
                'form': form,
                'records': records,
                'start_date': start_date,
                'end_date': end_date,
                'user': user,
            }
            return render(request, self.template_name, context)
        return render(request, self.template_name, {'form': form})
    



class ExUpdateList(View):
    def get(self,request,*args,**kwargs):
        user = request.user
        update = DailyUpdateModel.objects.filter(user = user)
        return render(request,"ExUpdateList.html",{"update":update})