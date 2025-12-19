from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone
import random
from django.core.mail import send_mail


# Create your models here.


class Teacher(models.Model):
    full_name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='instructors/', blank=True, null=True)

    expertise = models.CharField(
        max_length=255,
        help_text="Masalan: Python, Frontend, Data Science"
    )

    experience_years = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.full_name



class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True)
    
    class Meta:
        ordering = ['title']
        
    def __str__(self):
        return self.title


class Course(models.Model):
    owner = models.ForeignKey(Teacher,related_name='courses',on_delete=models.SET_NULL,null=True)
    subject = models.ForeignKey(Subject,related_name='courses',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True)
    overview = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

    
    


class Module(models.Model):
    course = models.ForeignKey(Course,related_name='modules',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    overview = models.TextField(null=True,blank=True)
    
    def __str__(self):
        return self.title


class Content(models.Model):
    module = models.ForeignKey(Module,related_name='contents',on_delete=models.CASCADE)
    
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            "model__in":(
                'text',
                'video',
                'image',
                'file'
            )
        }
    )
    
    object_id = models.PositiveIntegerField()

    item = GenericForeignKey(
        'content_type',
        'object_id'
    )
    


class ItemBase(models.Model):
    owner = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class Text(ItemBase):
    content = models.TextField() 
    
class File(ItemBase):
    file = models.FileField(upload_to='files')


class Video(ItemBase):
    url = models.URLField()

class Image(ItemBase):
    image = models.ImageField(upload_to='images')




class User(AbstractUser):
   
    groups = models.ManyToManyField(
        Group,
        related_name='upskill_user_set',  # auth.User bilan to'qnashmasligi uchun
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='upskill_user_permissions',  # auth.User bilan to'qnashmasligi uchun
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


def send_verification_code(user):
    code = str(random.randint(100000, 999999))
    user.email_code = code
    user.code_created_at = timezone.now()
    user.save()

    send_mail(
        'Tasdiqlash kodi',
        f'Sizning tasdiqlash kodingiz: {code}\nKod 5 daqiqa amal qiladi.',
        'noreply@gmail.com',
        [user.email],
    )
