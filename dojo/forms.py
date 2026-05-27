from django import forms
from django.contrib.auth.models import User

from .models import (
    Achievement,
    Group,
    PointEvent,
    Profile,
    Student,
    StudentAchievement,
)


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name',)
        labels = {
            'name': 'Название группы',
        }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-input',
                    'placeholder': 'Например: Дети группа 1',
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()

        if not name:
            raise forms.ValidationError('Название группы обязательно.')

        return name


class PointEventForm(forms.ModelForm):
    class Meta:
        model = PointEvent
        fields = ('points', 'comment')
        labels = {
            'points': 'Количество очков',
            'comment': 'Комментарий',
        }
        widgets = {
            'points': forms.NumberInput(
                attrs={
                    'class': 'form-input',
                    'placeholder': 'Например: 30',
                }
            ),
            'comment': forms.Textarea(
                attrs={
                    'class': 'form-input form-textarea',
                    'placeholder': 'Например: Выучил бросок через бедро',
                    'rows': 4,
                }
            ),
        }

    def clean_comment(self):
        comment = self.cleaned_data.get('comment', '').strip()

        if not comment:
            raise forms.ValidationError('Комментарий обязателен.')

        return comment

    def clean_points(self):
        points = self.cleaned_data.get('points')

        if points is None:
            raise forms.ValidationError('Укажи количество очков.')

        if points == 0:
            raise forms.ValidationError('Нельзя начислить 0 очков.')

        return points


class StudentAchievementForm(forms.ModelForm):
    class Meta:
        model = StudentAchievement
        fields = ('achievement',)
        labels = {
            'achievement': 'Достижение',
        }
        widgets = {
            'achievement': forms.Select(
                attrs={
                    'class': 'form-input',
                }
            ),
        }

    def __init__(self, *args, student=None, **kwargs):
        super().__init__(*args, **kwargs)

        if student is not None:
            awarded_ids = student.student_achievements.values_list(
                'achievement_id',
                flat=True,
            )

            self.fields['achievement'].queryset = Achievement.objects.exclude(
                id__in=awarded_ids
            )


class StudentCreateForm(forms.Form):
    username = forms.CharField(
        label='Логин ученика',
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Например: ivan_petrov',
            }
        )
    )
    password = forms.CharField(
        label='Пароль ученика',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Минимум 8 символов',
            }
        )
    )
    first_name = forms.CharField(
        label='Имя',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Иван',
            }
        )
    )
    last_name = forms.CharField(
        label='Фамилия',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Петров',
            }
        )
    )
    age = forms.IntegerField(
        label='Возраст',
        min_value=3,
        max_value=100,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-input',
                'placeholder': '12',
            }
        )
    )
    belt = forms.ChoiceField(
        label='Пояс',
        choices=Student.BELT_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-input',
            }
        )
    )

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким логином уже есть.')

        return username

    def clean_password(self):
        password = self.cleaned_data.get('password', '')

        if len(password) < 8:
            raise forms.ValidationError('Пароль должен быть минимум 8 символов.')

        return password


class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'age', 'belt')
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'age': 'Возраст',
            'belt': 'Пояс',
        }
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-input',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-input',
                }
            ),
            'age': forms.NumberInput(
                attrs={
                    'class': 'form-input',
                }
            ),
            'belt': forms.Select(
                attrs={
                    'class': 'form-input',
                }
            ),
        }

    def clean_age(self):
        age = self.cleaned_data.get('age')

        if age < 3 or age > 100:
            raise forms.ValidationError('Возраст должен быть от 3 до 100.')

        return age


class StudentPasswordChangeForm(forms.Form):
    password = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Минимум 8 символов',
            }
        )
    )
    password_repeat = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Введите пароль ещё раз',
            }
        )
    )

    def clean_password(self):
        password = self.cleaned_data.get('password', '')

        if len(password) < 8:
            raise forms.ValidationError('Пароль должен быть минимум 8 символов.')

        return password

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password_repeat = cleaned_data.get('password_repeat')

        if password and password_repeat and password != password_repeat:
            raise forms.ValidationError('Пароли не совпадают.')

        return cleaned_data


class StudentAvatarForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('avatar_emoji',)
        labels = {
            'avatar_emoji': 'Выберите аватар',
        }
        widgets = {
            'avatar_emoji': forms.RadioSelect(
                attrs={
                    'class': 'avatar-radio-list',
                }
            ),
        }