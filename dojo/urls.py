from django.urls import path

from . import views

app_name = 'dojo'

urlpatterns = [
    path('', views.index, name='index'),

    path('coach/', views.coach_dashboard, name='coach_dashboard'),
    path(
        'coach/groups/create/',
        views.group_create,
        name='group_create'
    ),
    path(
        'coach/groups/<int:group_id>/',
        views.coach_group_detail,
        name='coach_group_detail'
    ),
    path(
        'coach/groups/<int:group_id>/edit/',
        views.group_edit,
        name='group_edit'
    ),
    path(
        'coach/groups/<int:group_id>/delete/',
        views.group_delete,
        name='group_delete'
    ),
    path(
        'coach/groups/<int:group_id>/students/create/',
        views.student_create,
        name='student_create'
    ),
    path(
        'coach/students/<int:student_id>/',
        views.coach_student_detail,
        name='coach_student_detail'
    ),
    path(
        'coach/students/<int:student_id>/edit/',
        views.student_edit,
        name='student_edit'
    ),
    path(
        'coach/students/<int:student_id>/password/',
        views.student_password_change,
        name='student_password_change'
    ),
    path(
        'coach/students/<int:student_id>/delete/',
        views.student_delete,
        name='student_delete'
    ),
    path(
        'coach/students/<int:student_id>/points/add/',
        views.point_event_create,
        name='point_event_create'
    ),
    path(
        'coach/points/<int:event_id>/edit/',
        views.point_event_edit,
        name='point_event_edit'
    ),
    path(
        'coach/points/<int:event_id>/delete/',
        views.point_event_delete,
        name='point_event_delete'
    ),
    path(
        'coach/students/<int:student_id>/achievements/add/',
        views.student_achievement_create,
        name='student_achievement_create'
    ),
    path(
        'coach/student-achievements/<int:student_achievement_id>/delete/',
        views.student_achievement_delete,
        name='student_achievement_delete'
    ),

    path('student/me/', views.student_my_profile, name='student_my_profile'),
    path(
        'student/avatar/',
        views.student_avatar_update,
        name='student_avatar_update'
    ),
]