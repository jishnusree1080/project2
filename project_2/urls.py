"""project_2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from my_work import views
from project_2 import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("register/",views.EmployeeReg.as_view(),name="register"),
    path("control/home/",views.AdminHome.as_view(),name="admin_home"),
    path("exicutive/home/",views.ExicutiveHome.as_view(),name="ex_home"),
    path("emp/home/",views.EmployeeHome.as_view(),name="emp_home"),
    path("login/",views.CustomLoginView.as_view(),name="lgn"),
    path('add-default-attendance/', views.AddDefaultAttendanceView.as_view(), name='add_default_attendance'),
    path('update-checkout/', views.UpdateCheckoutView.as_view(), name='update_checkout'),
    path('add?/efault/attendance/', views.EXicutiveDefaultAttendanceView.as_view(), name='ex_add_default_attendance'),
    path('update?/checkout/', views.ExicutiveUpdateCheckoutView.as_view(), name='ex_update_checkout'),
    path('apply/leave/', views.LeaveRequest.as_view(), name='apply_leave'),
    path('apply/Ex/leave/', views.ExLeaveRequest.as_view(), name='Ex_apply_leave'),
    path("",views.Signout.as_view(),name="lgout"),
    path("leave/conform/<int:pk>",views.LeaveConFormation.as_view(),name="conform_leave"),
    path("leave/status/",views.LeaveStatus.as_view(),name="leave_status"),
    path("leave/ex/status/",views.ExLeaveStatus.as_view(),name="Exleave_status"),
    path("list/holidays/",views.ListHolidays.as_view(),name="list_holiday"),
    path('attendance/monthly/', views.MonthlyAttendanceView.as_view(), name='monthly_attendance'),
    path('attendance/monthly-statement/', views.MonthlyStatementView.as_view(), name='monthly_statement'),
    path('attendance/single/statement/<int:pk>', views.SingleMonthlyStatementView.as_view(), name='monthly_single_statement'),
    path('list/user/',views.EmployeeList.as_view(),name="emp_list"),
    path("my/attendance/",views.MyAttendence.as_view(),name="my_attendance"),
    path("emp/own/attendence/",views.EmployeeMonthlyAttendence.as_view(),name="emp_monthly_attendence"),
    path('monthly/list/attendance/', views.MonthlyAttendanceList.as_view(), name='monthly-attendance'),
    path("duty/progress/",views.DutyOnprogress.as_view(),name="duty_progress"),
    path("add/profile/",views.ProfileCreation.as_view(),name="profile"),
    path("profile/view/",views.ProfileListView.as_view(),name="prof_view"),
    path("add/general/holiday/",views.GeneralLeaveView.as_view(),name="add_leave"),
    path("list/holiday/",views.GeneralLeaveList.as_view(),name="list_leave"),
    path("add/daily/task/",views.DailyTaskUpdate.as_view(),name="add_daily_task"),
    path("list/task/",views.DailyTaskList.as_view(),name="list_task"),
    path("update/add/exicutive/",views.DailyExicutiveUpdate.as_view(),name="add_update"),
    path("update/list/exicutive/",views.AllUpdates.as_view(),name="list_update"),
    path("update/list/int/<int:pk>",views.singleUpdates.as_view(),name="single_update"),
    path("update/remark/int/<int:pk>",views.RemarkUpdate.as_view(),name="remark_update"),
    path("get/leave/",views.GetLeaveRequest.as_view(),name="all_leave"),
    # path('filter-weekly-updates/', views.WeeklyUpdatesView.as_view(), name='filter_weekly_updates'),
    path("add/expence/",views.AddExpence.as_view(),name="exp"),
    path("pending/expence/",views.PendingExpence.as_view(),name="pending_exp"),
    path("accepted/expenses/",views.AcceptedExpence.as_view(),name="accepted_exp"),
    path("rejected/expences/",views.RejectedExpence.as_view(),name="rejected_exp"),
    path("accept/exp/<int:pk>",views.AcceptExpence.as_view(),name="accp_exp"),
    path("reject/exp<int:pk>",views.RejectExpence.as_view(),name="rjt_exp"),
    path("expence/list/",views.ExpenceView.as_view(),name="exp_list"),
    path("monthly/update/",views.MonthlyUpdateList.as_view(),name="update_list"),
    path("weekly/update/",views.WeeklyUpdateList.as_view(),name="weekly_update"),
    path("ex/update/list/",views.ExUpdateList.as_view(),name="ex_update_list")
    


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



