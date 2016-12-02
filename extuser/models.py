from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.contrib.auth.models import Group
from decimal import *
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Email непременно должен быть указан')
        user = self.model(
            email=UserManager.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Role(models.Model):
    class Meta():
        db_table = 'role'
    title = models.CharField('Имя', max_length=50, blank=False)
    group = models.ManyToManyField(Group, related_name='roles')

    def __str__(self):
        return self.title

class ExtUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        'Электронная почта',
        max_length=255,
        unique=True,
        db_index=True
    )
    avatar = models.ImageField(
        'Аватар',
        blank=True,
        null=True,
        upload_to="user/avatar"
    )
    avatar_icon = models.ImageField(
        upload_to="user/avatar/icon",
        blank=True
    )
    firstname = models.CharField(
        'Имя',
        max_length=40,
        null=True,
        blank=True
    )
    lastname = models.CharField(
        'Фамилия',
        max_length=40,
        null=True,
        blank=True
    )
    middlename = models.CharField(
        'Отчество',
        max_length=40,
        null=True,
        blank=True
    )
    date_of_birth = models.DateField(
        'Дата рождения',
        null=True,
        blank=True
    )
    show_date_of_birth = models.BooleanField(
        'Показывать д.р.',
        default=True
    )
    register_date = models.DateField(
        'Дата регистрации',
        auto_now_add=True
    )
    is_active = models.BooleanField(
        'Активен',
        default=True
    )
    is_admin = models.BooleanField(
        'Суперпользователь',
        default=False
    )

    staff = models.BooleanField(
        'Сотрудник',
        default=False
    )

    oklad = models.PositiveIntegerField(
        default=0,
        blank=True,
        null=True
    )
    roles = models.ManyToManyField(Role, related_name='users')

    is_low = models.NullBooleanField()
    is_middle = models.NullBooleanField()
    is_top = models.NullBooleanField()
    is_emaigenerated = models.NullBooleanField(default=False)
    date_post = models.DateField(auto_now_add=True, null=True)


    # Определение сотрудник (в штате) или нет
    def make_is_staff(self):
        if self.groups.filter(name='staff'):
            self.staff = True
        else:
            self.staff = False
        self.save()

    # Этот метод обязательно должен быть определён
    def get_full_name(self):
        return self.email

    # Требуется для админки
    @property
    def is_staff(self):
        return self.is_admin

    def get_short_name(self):
        return self.email

    def __str__(self):
        email = ''
        firstname = ''
        lastname = ''
        if not self.is_emaigenerated:
            email = '(' + self.email + ')'
        if self.firstname:
            firstname = self.firstname
        if self.lastname:
            lastname = self.lastname
        if firstname and lastname:
            name = lastname + ' ' + firstname
        else:
            name = lastname + ' ' + firstname + ' ' + email
        return name

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Emails(models.Model):
    class Meta():
        db_table = 'emails'
    extuser = models.ForeignKey(ExtUser, on_delete=models.CASCADE)
    email = models.EmailField(verbose_name='Доп. почта', blank=False)

    def __str__(self):
        return str(self.email)

class PhoneNumber(models.Model):
    class Meta():
        db_table = 'ext_phone_number'
    extuser = models.ForeignKey(ExtUser, on_delete=models.CASCADE)
    number = models.CharField(verbose_name='Номер телефона', max_length=20, blank=False)

    def __str__(self):
        return str(self.number)
