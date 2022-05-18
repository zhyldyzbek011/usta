from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

from django.utils.translation import gettext_lazy as _









class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('The given email must be set!')
        email = self.normalize_email(email=email)
        user = self.model(email=email, **kwargs)
        user.create_activation_code()
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **kwargs):
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)
        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must have status is_staff=True')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have status is_superuser=True')
        return self._create_user(email, password, **kwargs)


class CustomUser(AbstractUser):
    email = models.EmailField('email addres', unique=True)
    password = models.CharField(max_length=100)
    activation_code = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active.'
            'Unselect this instead of deleting accounts.'), )

    def __str__(self) -> str:
        return self.email

    def create_activation_code(self):
        import uuid
        code = str(uuid.uuid4())
        self.activation_code = code


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=150, default='Разные')

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return f'{self.name}'


class Location(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self): return self.name


class Worker_card(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    body = models.TextField(blank=True)
    phone_number = models.CharField(max_length=13)
    profil = models.ImageField(upload_to='images/', blank=True)
    owner = models.ForeignKey(User, related_name='card', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='card')
    location = models.ForeignKey(Location, related_name='location', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return f'{self.owner} - {self.first_name} {self.last_name}'


class Worker_cardImages(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='images/')
    card = models.ForeignKey(Worker_card, on_delete=models.CASCADE, related_name='card')
    class Meta:
        verbose_name = 'image'
        verbose_name_plural = 'images'

    @staticmethod
    def generate_name():
        import random
        return 'image' + str(random.randint(100000, 999999))

    def save(self, *args, **kwargs):
        self.title = self.generate_name()
        return super(Worker_cardImages, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.title} -> {self.card.id}'


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    card = models.ForeignKey(Worker_card,on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.owner} -> {self.card} -> {self.created_at}'


class Likes(models.Model):
    card = models.ForeignKey(Worker_card, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE,  related_name='liked')

    class Meta:
        unique_together = ['card', 'user']