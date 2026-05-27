from django.db.models import Sum


RANKS = [
    {
        'name': 'Бронза',
        'min_points': 0,
        'max_points': 199,
    },
    {
        'name': 'Серебро',
        'min_points': 200,
        'max_points': 499,
    },
    {
        'name': 'Золото',
        'min_points': 500,
        'max_points': 899,
    },
    {
        'name': 'Платина',
        'min_points': 900,
        'max_points': 1399,
    },
    {
        'name': 'Алмаз',
        'min_points': 1400,
        'max_points': 1999,
    },
    {
        'name': 'Мастер',
        'min_points': 2000,
        'max_points': 2999,
    },
    {
        'name': 'Легенда',
        'min_points': 3000,
        'max_points': None,
    },
]


def get_rank_info(total_points):
    current_rank = RANKS[0]
    next_rank = None

    for index, rank in enumerate(RANKS):
        max_points = rank['max_points']

        if max_points is None or total_points <= max_points:
            current_rank = rank

            if index + 1 < len(RANKS):
                next_rank = RANKS[index + 1]

            break

    if next_rank is None:
        return {
            'name': current_rank['name'],
            'next_rank': None,
            'points_to_next': 0,
            'progress_percent': 100,
        }

    current_min = current_rank['min_points']
    next_min = next_rank['min_points']
    rank_range = next_min - current_min
    points_inside_rank = total_points - current_min

    progress_percent = int((points_inside_rank / rank_range) * 100)
    progress_percent = max(0, min(progress_percent, 100))

    return {
        'name': current_rank['name'],
        'next_rank': next_rank['name'],
        'points_to_next': next_min - total_points,
        'progress_percent': progress_percent,
    }


def recalculate_student_points(student):
    total_points = student.point_events.aggregate(
        total=Sum('points')
    )['total'] or 0

    student.total_points = total_points
    student.save(update_fields=['total_points'])

    return total_points


def get_group_rating(group):
    return group.students.select_related('user').order_by(
        '-total_points',
        'first_name',
        'last_name',
    )


def get_group_students_by_name(group):
    return group.students.select_related('user').order_by(
        'first_name',
        'last_name',
    )


def get_student_place(student):
    better_students_count = student.group.students.filter(
        total_points__gt=student.total_points
    ).count()

    return better_students_count + 1