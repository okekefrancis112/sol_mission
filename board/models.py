# from tokenize import blank_re
from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.urls import reverse
# from platformdirs import user_cache_dir
from ckeditor.fields import RichTextField 
from django.utils import timezone
from uuid import uuid4
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.humanize.templatetags import humanize
# from cloudinary.models import CloudinaryField


# Create your models here.

class CustomAccountManager(BaseUserManager):
    def create_user(self, email, user_name, first_name, last_name, password, **other_fields):
        
        if not email:
            raise ValueError(_('You must provide an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, 
                          first_name=first_name, last_name=last_name,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, user_name, first_name, last_name, password, **other_fields):
        
        other_fields.setdefault('is_superuser',True)
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_active',True)
        
        if other_fields.get('is_superuser') is not True:
                raise ValueError(_('Superuser must be assigned to is_superuser=True.'))

        if other_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must be assigned to is_staff=True.'))
        
        return self.create_user(email, user_name, first_name, last_name, password, **other_fields)


class NewUser(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(_("about"), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    
    objects = CustomAccountManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name', 'last_name']
    
    def __str__(self):
        return self.user_name
    
    
User = get_user_model()

class Board(models.Model):
    title = models.CharField(max_length=255)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    description = RichTextField(blank=True, null=True)
    # body = models.TextField()
    image = models.ImageField(null=True, blank = True, upload_to = "images/")
    
    def __str__(self):
        return self.title + '|' + str(self.member)
    
class Category(models.Model):
    title = models.CharField(null=True, blank=True, max_length=200)
    
    uniqueId = models.CharField(null=True, blank=True, max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
      return '{}'.format(self.title)
    
    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{}{}'.format(self.title, self.uniqueId))
            
        self.slug = slugify('{}{}'.format(self.title, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())
        super(Category, self).save(*args, **kwargs)
        
    
    
    
class Mission(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(null=True, blank = True, upload_to = "missions/")
    
    category = models.ForeignKey(Category, null=True, blank=True, max_length=300, on_delete=models.CASCADE)
    
    # created_at = models.DateTimeField(auto_now_add=True)
    uniqueId = models.CharField(null=True, blank=True, max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
    #   return '{} {}'.format(self.name, self.uniqueId)
        return f"{self.name}"
    
    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{}{}'.format(self.name, self.uniqueId))
            
        self.slug = slugify('{}{}'.format(self.name, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())
        super(Mission, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse("mission_detail", kwargs={"slug": self.slug})
           
        
        
class Image(models.Model):
    description = models.TextField(null=True, blank=True)
    altText = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank = True, upload_to = "mission_fields")
    
    mission = models.ForeignKey(Mission, null=True, blank=True, on_delete=models.CASCADE, related_name= 'mission_image')
    
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"Images from {self.mission} Mission"
    
    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{}{}'.format(self.mission.name, self.uniqueId))
            
        self.slug = slugify('{}{}'.format(self.mission.name, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())
        super(Image, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse("image_detail", kwargs={"slug": self.slug})
          
        
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')
    

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.CharField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = RichTextField(blank=True, null=True)
    image = models.ImageField(null=True, blank = True, upload_to = "blog/")
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    objects = models.Manager()
    published = PublishedManager()
    
    class Meta:
        ordering = ('-publish',)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        args = [
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug,
                ]
        return reverse('blog_detail', args=args)
    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)   
    
    class Meta:
        ordering = ('date_added',)
    
    def __str__(self):
        return "Comment by {} on {}".format(self.name, self.post)
    
  


class Payment(models.Model):
    name = models.CharField(max_length=250)
    phone_number = models.PositiveIntegerField()
    village = models.CharField(max_length=100, default='Village')
    amount = models.PositiveIntegerField()
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    ref = models.CharField(max_length=200)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    
    
    
    class Meta:
        ordering = ('-date_created',)
        
    def __str__(self):
        return f"{self.name} made a donation of #{self.amount} to {self.village} on {self.date_created}"
        
    
    def save(self, *args, **kwargs):
        if not self.date_created:
            self.date_created = timezone.localtime(timezone.now())
            self.date_created.strftime("%m-%d-%Y, %H:%M:%S")
            # humanize.naturaltime(self.date_created)
            # print(self.date_created)
            
        if not self.verified:
            self.verified=True
        
        super(Payment, self).save(*args, **kwargs)
    

    
    

    
    
