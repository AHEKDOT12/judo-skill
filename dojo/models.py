from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    ROLE_COACH = 'coach'
    ROLE_STUDENT = 'student'

    ROLE_CHOICES = [
        (ROLE_COACH, 'Тренер'),
        (ROLE_STUDENT, 'Ученик'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        verbose_name='Роль'
    )

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'{self.user.username} — {self.get_role_display()}'


class Group(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название группы'
    )
    coach = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='judo_groups',
        verbose_name='Тренер'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ['name']

    def __str__(self):
        return self.name


class Student(models.Model):
    BELT_WHITE = 'white'
    BELT_YELLOW = 'yellow'
    BELT_ORANGE = 'orange'
    BELT_GREEN = 'green'
    BELT_BLUE = 'blue'
    BELT_BROWN = 'brown'
    BELT_BLACK = 'black'

    BELT_CHOICES = [
        (BELT_WHITE, 'Белый'),
        (BELT_YELLOW, 'Жёлтый'),
        (BELT_ORANGE, 'Оранжевый'),
        (BELT_GREEN, 'Зелёный'),
        (BELT_BLUE, 'Синий'),
        (BELT_BROWN, 'Коричневый'),
        (BELT_BLACK, 'Чёрный'),
    ]

    AVATAR_CHOICES = [
        ('🥋', '🥋 Дзюдо'),
        ('💪', '💪 Сила'),
        ('🔥', '🔥 Огонь'),
        ('⚡', '⚡ Молния'),
        ('🦁', '🦁 Лев'),
        ('🐺', '🐺 Волк'),
        ('🐯', '🐯 Тигр'),
        ('🦅', '🦅 Орёл'),
        ('🐻', '🐻 Медведь'),
        ('🛡️', '🛡️ Щит'),
        ('⚔️', '⚔️ Мечи'),
        ('🏆', '🏆 Кубок'),
        ('🥇', '🥇 Золото'),
        ('🥈', '🥈 Серебро'),
        ('🥉', '🥉 Бронза'),
        ('🎯', '🎯 Цель'),
        ('🚀', '🚀 Ракета'),
        ('🌪️', '🌪️ Вихрь'),
        ('🧠', '🧠 Ум'),
        ('🗿', '🗿 Стойкость'),
        ('🏋️', '🏋️ Силач'),
        ('🤼', '🤼 Борьба'),
        ('🏃', '🏃 Скорость'),
        ('🧗', '🧗 Упорство'),
        ('🥊', '🥊 Боец'),
        ('👊', '👊 Удар'),
        ('✊', '✊ Характер'),
        ('🤜', '🤜 Напор'),
        ('🤛', '🤛 Ответ'),
        ('🦾', '🦾 Железная рука'),
        ('😤', '😤 Настрой'),
        ('😎', '😎 Уверенность'),
        ('🧘', '🧘 Самоконтроль'),
        ('🌟', '🌟 Звезда'),
        ('💎', '💎 Алмаз'),
        ('👑', '👑 Король'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile',
        verbose_name='Аккаунт ученика'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='students',
        verbose_name='Группа'
    )
    first_name = models.CharField(
        max_length=100,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name='Фамилия'
    )
    age = models.PositiveSmallIntegerField(
        verbose_name='Возраст'
    )
    total_points = models.IntegerField(
        default=0,
        verbose_name='Всего очков'
    )
    belt = models.CharField(
        max_length=20,
        choices=BELT_CHOICES,
        default=BELT_WHITE,
        verbose_name='Пояс'
    )
    avatar_emoji = models.CharField(
        max_length=10,
        choices=AVATAR_CHOICES,
        default='🥋',
        verbose_name='Аватар'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class PointEvent(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='point_events',
        verbose_name='Ученик'
    )
    coach = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_point_events',
        verbose_name='Тренер'
    )
    points = models.IntegerField(
        verbose_name='Очки'
    )
    comment = models.TextField(
        verbose_name='Комментарий'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата начисления'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения'
    )

    class Meta:
        verbose_name = 'Начисление очков'
        verbose_name_plural = 'Начисления очков'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.student}: {self.points} очков'


class Achievement(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Название'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Иконка'
    )

    class Meta:
        verbose_name = 'Достижение'
        verbose_name_plural = 'Достижения'
        ordering = ['title']

    def __str__(self):
        return self.title


class StudentAchievement(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='student_achievements',
        verbose_name='Ученик'
    )
    achievement = models.ForeignKey(
        Achievement,
        on_delete=models.CASCADE,
        related_name='student_achievements',
        verbose_name='Достижение'
    )
    awarded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Кем выдано'
    )
    awarded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата выдачи'
    )

    class Meta:
        verbose_name = 'Достижение ученика'
        verbose_name_plural = 'Достижения учеников'
        unique_together = ('student', 'achievement')
        ordering = ['-awarded_at']

    def __str__(self):
        return f'{self.student} — {self.achievement}'