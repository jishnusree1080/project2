from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin,User
from django.core.validators import FileExtensionValidator




class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Username must contain only letters, numbers, and @/./+/-/_ characters.'
        )]
    )
    first_name = models.CharField(max_length=200,null=True)
    last_name = models.CharField(max_length=200,null=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    ROLL_CHOICES = [
        ('staff', 'staff'),
        ('exicutive', 'exicutive'),
        
    ]
    user_type=models.CharField(max_length=20, choices=ROLL_CHOICES, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)


    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

   
    

    def __str__(self):
        return self.username





class Attendancedb(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    checkin = models.TimeField(null=True)
    checkout = models.TimeField(null=True)
    start = models.BooleanField(default=False)
    end = models.BooleanField(default=False)
    

    def get_monthly_data(self, user, month, year):
        return Attendancedb.objects.filter(
            user=user,
            date__year=year,
            date__month=month
        )

class LeaveUpdate(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    date = models.DateField(null = True)
    reason = models.TextField()
    status = models.BooleanField(default=False)
    created_at = models.DateField(auto_now=True,null=True)



class GeneralHolidays(models.Model):
    date = models.DateField()
    reason = models.TextField(null=True)



class StaffProfile(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    mobile = models.CharField(
        max_length=14,
        validators=[RegexValidator(
            regex=r'^\+91\d{10}$',
            message="Phone number must be entered in the format: '+91XXXXXXXXXX' and must be exactly 14 characters long."
        )],
        blank=True,
        null=True
    )
    date_of_birth = models.DateField(null=True)
    permenant_address = models.TextField()
    current_address = models.TextField()
    qualification = models.CharField(max_length=200,null=True)
    bank_name = models.CharField(max_length=200,null=True)
    ac_no = models.PositiveIntegerField(null=True)
    ifsc_code = models.CharField(max_length=15,null=True)
    branch = models.CharField(max_length=100,null=True)
    age = models.PositiveBigIntegerField()
    father_name = models.CharField(max_length=50)
    mothers_name = models.CharField(max_length=50)
    spouse_name = models.CharField(max_length=50,null=True,blank=True)
    married = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    status1 = models.BooleanField(default=False)




    # class DailyWorkModel(models.Model):
    #     user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    #     date = models.DateField()
    #     time = models.TimeField()
    #     work = models.TextField()
    #     status = models.BooleanField(default=False)
    #     created_at = models.DateTimeField(auto_now=True)


class DailyTaskModel(models.Model):
    date = models.DateField()
    time = models.CharField(max_length=25)
    task = models.TextField()
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    link = models.URLField(null=True)
    staus = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)



class DailyUpdateModel(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    date = models.DateField(null=True )
    college_name = models.CharField(max_length=250)
    suggessions = models.TextField()
    feed_back = models.TextField()
    remark = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    created_at = models.DateTimeField(auto_now=True)


 
class ExpenceModel(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    date = models.DateField(null=True)
    college = models.CharField(max_length=200)
    
    ROLL_CHOICES = [
        ('private_vehicle', 'private_vehicle'),
        ('public_transport', 'public_transport'),
        ('company_vehicle', 'company_vehicle'),
        ('others', 'others'),
        
    ]
    transport=models.CharField(max_length=20, choices=ROLL_CHOICES, null=True, blank=True)
    ticket = models.FileField(upload_to='poster/', validators=[FileExtensionValidator(['pdf', 'jpg', 'png','jpeg'])],null=True,blank=True)
    fuel_receipt = models.FileField(upload_to='poster/', validators=[FileExtensionValidator(['pdf', 'jpg', 'png','jpeg'])],null=True,blank=True)
    food_bill = models.FileField(upload_to='poster/', validators=[FileExtensionValidator(['pdf', 'jpg', 'png','jpeg'])],null=True,blank=True)
    others = models.FileField(upload_to='poster/', validators=[FileExtensionValidator(['pdf', 'jpg', 'png','jpeg'])],null=True,blank=True)
    expense = models.PositiveBigIntegerField()
    approve = models.BooleanField(default=False)
    reject = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)