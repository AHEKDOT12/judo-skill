from django.contrib.auth.decorators import user_passes_test


def is_coach(user):
    return (
        user.is_authenticated
        and hasattr(user, 'profile')
        and user.profile.role == 'coach'
    )


def is_student(user):
    return (
        user.is_authenticated
        and hasattr(user, 'profile')
        and user.profile.role == 'student'
    )


coach_required = user_passes_test(
    is_coach,
    login_url='accounts:login',
)

student_required = user_passes_test(
    is_student,
    login_url='accounts:login',
)