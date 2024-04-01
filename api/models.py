from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db.models.signals import post_save


class UserManager(BaseUserManager):
    def create_user(self, email, name, tc, password=None, password2=None):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            email = self.normalize_email(email),
            name = name,
            tc = tc
        )
        user.set_password(password)
        user.save(using=self.db)
        return user
    def create_superuser(self, email, name, tc, password=None):
        user = self.create_user(
            email,
            name=name,
            password=password,
            tc=tc
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=200)
    tc = models.BooleanField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['name','tc']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class PersonalInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=200)
    lname = models.CharField(max_length=200)
    gender = models.CharField(max_length=1)
    contact = models.IntegerField()
    dob = models.DateField(max_length=8)
    address = models.CharField(max_length=500)

    def __str__(self):
        return self.fname

class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    education = models.CharField(max_length=50)
    board = models.CharField(max_length=100) 
    passing_out_year = models.IntegerField()
    total_marks = models.IntegerField()

    def __str__(self):
        return str(self.user)

class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100) 
    year_of_experience = models.IntegerField()
    joining_date = models.DateField(max_length=8) 
    resigning_date = models.DateField(max_length=8) 
    job_role = models.CharField(max_length=100)

    def __str__(self):
        return str(self.user)


class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skills = models.CharField(max_length=200) 

    def __str__(self):
        return str(self.user)


class  Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="static", default='static\profile.jpeg')

    def __str__(self):
        return str(self.user)

def created_profile(sender, instance, created, **kwargs):
    if created:
        Profile .objects.create(user=instance)
        print("Profile Created")
post_save.connect(created_profile, sender=User)

