from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import coach_required, student_required
from .forms import (
    GroupForm,
    PointEventForm,
    StudentAchievementForm,
    StudentCreateForm,
    StudentPasswordChangeForm,
    StudentUpdateForm,
    StudentAvatarForm,
)
from .models import Group, PointEvent, Profile, Student, StudentAchievement
from .services import (
    get_group_rating,
    get_group_students_by_name,
    get_rank_info,
    get_student_place,
    recalculate_student_points,
)

def index(request):
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        if request.user.profile.role == 'coach':
            return redirect('dojo:coach_dashboard')

        if request.user.profile.role == 'student':
            return redirect('dojo:student_my_profile')

    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('/admin/')

    return render(request, 'dojo/index.html')


@coach_required
def coach_dashboard(request):
    groups = Group.objects.filter(
        coach=request.user
    ).prefetch_related('students')

    return render(
        request,
        'dojo/coach_dashboard.html',
        {
            'groups': groups,
        }
    )


@coach_required
def group_create(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)

        if form.is_valid():
            group = form.save(commit=False)
            group.coach = request.user
            group.save()

            return redirect('dojo:coach_group_detail', group.id)
    else:
        form = GroupForm()

    return render(
        request,
        'dojo/group_form.html',
        {
            'form': form,
            'page_title': 'Создать группу',
            'button_text': 'Создать группу',
        }
    )


@coach_required
def group_edit(request, group_id):
    group = get_object_or_404(
        Group,
        id=group_id,
        coach=request.user,
    )

    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)

        if form.is_valid():
            form.save()

            return redirect('dojo:coach_group_detail', group.id)
    else:
        form = GroupForm(instance=group)

    return render(
        request,
        'dojo/group_form.html',
        {
            'form': form,
            'group': group,
            'page_title': 'Редактировать группу',
            'button_text': 'Сохранить изменения',
        }
    )


@coach_required
def group_delete(request, group_id):
    group = get_object_or_404(
        Group.objects.prefetch_related('students'),
        id=group_id,
        coach=request.user,
    )

    if request.method == 'POST':
        group.delete()

        return redirect('dojo:coach_dashboard')

    return render(
        request,
        'dojo/group_confirm_delete.html',
        {
            'group': group,
        }
    )


@coach_required
def coach_group_detail(request, group_id):
    group = get_object_or_404(
        Group.objects.prefetch_related('students'),
        id=group_id,
        coach=request.user,
    )

    active_sort = request.GET.get('sort', 'points')

    if active_sort == 'name':
        students = get_group_students_by_name(group)
    else:
        active_sort = 'points'
        students = get_group_rating(group)

    students_with_rank = []

    for student in students:
        students_with_rank.append(
            {
                'student': student,
                'rank_info': get_rank_info(student.total_points),
            }
        )

    return render(
        request,
        'dojo/coach_group_detail.html',
        {
            'group': group,
            'students_with_rank': students_with_rank,
            'active_sort': active_sort,
        }
    )


@coach_required
def student_create(request, group_id):
    group = get_object_or_404(
        Group,
        id=group_id,
        coach=request.user,
    )

    if request.method == 'POST':
        form = StudentCreateForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                )

                Profile.objects.create(
                    user=user,
                    role=Profile.ROLE_STUDENT,
                )

                student = Student.objects.create(
                    user=user,
                    group=group,
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    age=form.cleaned_data['age'],
                    belt=form.cleaned_data['belt'],
                    total_points=0,
                )

            return redirect('dojo:coach_student_detail', student.id)
    else:
        form = StudentCreateForm()

    return render(
        request,
        'dojo/student_form.html',
        {
            'form': form,
            'group': group,
            'page_title': 'Добавить ученика',
            'button_text': 'Создать ученика',
        }
    )


@coach_required
def coach_student_detail(request, student_id):
    student = get_object_or_404(
        Student.objects.select_related('group', 'user'),
        id=student_id,
        group__coach=request.user,
    )

    point_events = student.point_events.select_related('coach')[:20]

    achievements = student.student_achievements.select_related(
        'achievement',
        'awarded_by',
    )

    rank_info = get_rank_info(student.total_points)
    place = get_student_place(student)

    return render(
        request,
        'dojo/coach_student_detail.html',
        {
            'student': student,
            'point_events': point_events,
            'achievements': achievements,
            'rank_info': rank_info,
            'place': place,
        }
    )


@coach_required
def student_edit(request, student_id):
    student = get_object_or_404(
        Student.objects.select_related('group', 'user'),
        id=student_id,
        group__coach=request.user,
    )

    if request.method == 'POST':
        form = StudentUpdateForm(request.POST, instance=student)

        if form.is_valid():
            updated_student = form.save()

            updated_student.user.first_name = updated_student.first_name
            updated_student.user.last_name = updated_student.last_name
            updated_student.user.save(update_fields=['first_name', 'last_name'])

            return redirect('dojo:coach_student_detail', updated_student.id)
    else:
        form = StudentUpdateForm(instance=student)

    return render(
        request,
        'dojo/student_form.html',
        {
            'form': form,
            'group': student.group,
            'student': student,
            'page_title': 'Редактировать ученика',
            'button_text': 'Сохранить изменения',
        }
    )

@coach_required
def student_password_change(request, student_id):
    student = get_object_or_404(
        Student.objects.select_related('group', 'user'),
        id=student_id,
        group__coach=request.user,
    )

    if request.method == 'POST':
        form = StudentPasswordChangeForm(request.POST)

        if form.is_valid():
            student.user.set_password(form.cleaned_data['password'])
            student.user.save(update_fields=['password'])

            return redirect('dojo:coach_student_detail', student.id)
    else:
        form = StudentPasswordChangeForm()

    return render(
        request,
        'dojo/student_password_form.html',
        {
            'form': form,
            'student': student,
        }
    )

@coach_required
def student_delete(request, student_id):
    student = get_object_or_404(
        Student.objects.select_related('group', 'user'),
        id=student_id,
        group__coach=request.user,
    )

    group = student.group
    user = student.user

    if request.method == 'POST':
        user.delete()

        return redirect('dojo:coach_group_detail', group.id)

    return render(
        request,
        'dojo/student_confirm_delete.html',
        {
            'student': student,
            'group': group,
        }
    )


@coach_required
def point_event_create(request, student_id):
    student = get_object_or_404(
        Student.objects.select_related('group'),
        id=student_id,
        group__coach=request.user,
    )

    if request.method == 'POST':
        form = PointEventForm(request.POST)

        if form.is_valid():
            point_event = form.save(commit=False)
            point_event.student = student
            point_event.coach = request.user
            point_event.save()

            recalculate_student_points(student)

            return redirect('dojo:coach_student_detail', student.id)
    else:
        form = PointEventForm()

    return render(
        request,
        'dojo/point_event_form.html',
        {
            'form': form,
            'student': student,
            'page_title': 'Начисление очков',
            'button_text': 'Сохранить начисление',
        }
    )


@coach_required
def point_event_edit(request, event_id):
    point_event = get_object_or_404(
        PointEvent.objects.select_related(
            'student',
            'student__group',
        ),
        id=event_id,
        student__group__coach=request.user,
    )

    student = point_event.student

    if request.method == 'POST':
        form = PointEventForm(request.POST, instance=point_event)

        if form.is_valid():
            form.save()
            recalculate_student_points(student)

            return redirect('dojo:coach_student_detail', student.id)
    else:
        form = PointEventForm(instance=point_event)

    return render(
        request,
        'dojo/point_event_form.html',
        {
            'form': form,
            'student': student,
            'page_title': 'Редактирование начисления',
            'button_text': 'Сохранить изменения',
        }
    )


@coach_required
def point_event_delete(request, event_id):
    point_event = get_object_or_404(
        PointEvent.objects.select_related(
            'student',
            'student__group',
        ),
        id=event_id,
        student__group__coach=request.user,
    )

    student = point_event.student

    if request.method == 'POST':
        point_event.delete()
        recalculate_student_points(student)

        return redirect('dojo:coach_student_detail', student.id)

    return render(
        request,
        'dojo/point_event_confirm_delete.html',
        {
            'point_event': point_event,
            'student': student,
        }
    )


@coach_required
def student_achievement_create(request, student_id):
    student = get_object_or_404(
        Student.objects.select_related('group'),
        id=student_id,
        group__coach=request.user,
    )

    if request.method == 'POST':
        form = StudentAchievementForm(request.POST, student=student)

        if form.is_valid():
            student_achievement = form.save(commit=False)
            student_achievement.student = student
            student_achievement.awarded_by = request.user
            student_achievement.save()

            return redirect('dojo:coach_student_detail', student.id)
    else:
        form = StudentAchievementForm(student=student)

    return render(
        request,
        'dojo/student_achievement_form.html',
        {
            'form': form,
            'student': student,
        }
    )


@coach_required
def student_achievement_delete(request, student_achievement_id):
    student_achievement = get_object_or_404(
        StudentAchievement.objects.select_related(
            'student',
            'student__group',
            'achievement',
        ),
        id=student_achievement_id,
        student__group__coach=request.user,
    )

    student = student_achievement.student

    if request.method == 'POST':
        student_achievement.delete()

        return redirect('dojo:coach_student_detail', student.id)

    return render(
        request,
        'dojo/student_achievement_confirm_delete.html',
        {
            'student_achievement': student_achievement,
            'student': student,
        }
    )


@student_required
def student_my_profile(request):
    student = get_object_or_404(
        Student.objects.select_related('group', 'user'),
        user=request.user,
    )

    point_events = student.point_events.select_related('coach')[:20]

    achievements = student.student_achievements.select_related(
        'achievement',
        'awarded_by',
    )

    rating = get_group_rating(student.group)
    rank_info = get_rank_info(student.total_points)
    place = get_student_place(student)

    return render(
        request,
        'dojo/student_my_profile.html',
        {
            'student': student,
            'point_events': point_events,
            'achievements': achievements,
            'rating': rating,
            'rank_info': rank_info,
            'place': place,
        }
    )

@student_required
def student_avatar_update(request):
    student = get_object_or_404(
        Student.objects.select_related('group', 'user'),
        user=request.user,
    )

    if request.method == 'POST':
        form = StudentAvatarForm(request.POST, instance=student)

        if form.is_valid():
            form.save()

            return redirect('dojo:student_my_profile')
    else:
        form = StudentAvatarForm(instance=student)

    return render(
        request,
        'dojo/student_avatar_form.html',
        {
            'form': form,
            'student': student,
        }
    )