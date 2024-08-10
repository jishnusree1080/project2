from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from my_work.models import *





class register(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=["username","first_name","last_name","password","email","user_type"]



class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class LeaveForm(forms.ModelForm):
    class Meta:
        model = LeaveUpdate
        fields = ["date","reason"]






import datetime

class MonthYearUserForm(forms.Form):
    year = forms.IntegerField(min_value=2000, max_value=2100, initial=datetime.date.today().year)
    month = forms.IntegerField(min_value=1, max_value=12, initial=datetime.date.today().month)
    user = forms.ModelChoiceField(queryset=CustomUser.objects.filter(is_superuser = False), required=False)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        fields = [
            'full_name', 'email', 'mobile', 'date_of_birth', 
            'permenant_address', 'current_address', 'qualification', 
            'bank_name', 'ac_no', 'ifsc_code', 'branch', 'age', 
            'father_name', 'mothers_name', 'spouse_name', 'married', 
            
        ]



class GeneralLeave(forms.ModelForm):
    class Meta:
        model = GeneralHolidays
        fields = ["date","reason"]



class UpdateForm(forms.ModelForm):
    class Meta:
        model = DailyUpdateModel
        fields = ["date","college_name","suggessions","feed_back"]




class DailyTskForm(forms.ModelForm):
     class Meta:
         model = DailyTaskModel
         fields = ["date","time","task","user","link"]


     def __init__(self, *args, **kwargs):
        super(DailyTskForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = CustomUser.objects.filter(is_superuser=False)



class RemarkUpdateForm(forms.ModelForm):
    class Meta:
        model = DailyUpdateModel
        fields = ["remark"]



class DateForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))



class ExpenceForm(forms.ModelForm):
    class Meta:
        model = ExpenceModel
        fields = ["date","college","expense","transport","ticket","fuel_receipt","food_bill","others",]



class DateRangeUserForm(forms.Form):
    start_date = forms.DateField(label='Start Date', widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='End Date', widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    user = forms.ModelChoiceField(queryset=CustomUser.objects.filter(is_superuser = False), required=False, label='User')
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        
        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError("End date should be greater than or equal to start date.")
        return cleaned_data