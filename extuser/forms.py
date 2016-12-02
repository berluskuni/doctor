
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from extuser.models import ExtUser

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Подтверждение',
        widget=forms.PasswordInput
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароль и подтверждение не совпадают')
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ('email',)

class RegistrationForm(forms.Form):
    years = []
    x = 2011
    for y in range(90):
        x -= 1
        years.append(x)
    CHOOSE_YEARS = tuple(years)
    email = forms.EmailField(required=False)
    firstname = forms.CharField(label='Имя', max_length=40, required=False)
    lastname = forms.CharField(label='Фамилия', max_length=40, required=False)
    password0 = forms.CharField(label='Текущий пароль', required=False, widget=forms.PasswordInput)
    password1 = forms.CharField(label='Новый пароль', required=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение', required=False, widget=forms.PasswordInput)
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=CHOOSE_YEARS), required=False)

class UserChangeForm(forms.ModelForm):

    '''
    Форма для обновления данных пользователей. Нужна только для того, чтобы не
    видеть постоянных ошибок "Не заполнено поле password" при обновлении данных
    пользователя.
    '''
    password = ReadOnlyPasswordHashField(
        widget=forms.PasswordInput,
        required=False
    )

    def save(self, commit=True):
        user = super(UserChangeForm, self).save(commit=False)
        password = self.cleaned_data["password"]
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ['email', ]