# Judo Skill

🌐 Language: **English** | [Русский](README.md)

**Judo Skill** is a Django web application for judo coaches. It helps track student progress through a gamified system of points, ranks, belts, achievements, emoji avatars, group ratings, and student accounts.

The project was built as a real MVP for a sports club. Coaches manage groups and students through the web interface, while students sign in to their personal account to follow their progress.

---

## Demo

**Website:** https://judoskill.dpdns.org/

---

## Project Idea

In many sports clubs, student progress is often tracked in a coach's memory, on paper, or in spreadsheets.

**Judo Skill** turns this workflow into a clear game-like system:

- the coach awards points for training, technique, discipline, competitions, and progress;
- the student sees their rank, group position, belt, achievements, and point history;
- the rating motivates students to train more consistently;
- achievements make the learning process feel more game-like;
- emoji avatars add personality without requiring photo uploads.

---

## Features

### Coach

A coach can:

- create, edit, and delete groups;
- add students to groups;
- edit student details;
- delete students;
- change a student's password;
- award points;
- edit and delete point events;
- assign achievements;
- remove assigned achievements;
- view the student ranking inside a group;
- sort students by points or by name;
- view each student's profile.

### Student

A student can:

- sign in to a personal account;
- see the current rank;
- see the total number of points;
- see progress toward the next rank;
- see the current belt;
- see their place in the group;
- see the group ranking;
- see recent point events;
- see earned achievements;
- change the emoji avatar.

---

## Rank System

The rank is calculated automatically from the student's total points.

| Rank | Points |
|---|---:|
| 🥉 Bronze | 0–199 |
| 🥈 Silver | 200–499 |
| 🥇 Gold | 500–899 |
| 💠 Platinum | 900–1399 |
| 💎 Diamond | 1400–1999 |
| 🧠 Master | 2000–2999 |
| 👑 Legend | 3000+ |

---

## Point System

The point system is designed so regular training gives steady small progress, while competitions, belt tests, and major achievements provide a larger boost.

| Action | Points |
|---|---:|
| Attended a training session | +5 |
| Worked well during training | +10 |
| Learned a basic technique | +15 |
| Performed a technique well | +20 |
| Used a technique in sparring | +35 |
| Participated in a competition | +50 |
| 3rd place in a competition | +120 |
| 2nd place in a competition | +160 |
| 1st place in a competition | +220 |
| Passed a belt test | +150 |
| New belt | +200 |
| Student of the month | +200 |

---

## Achievements

Achievements are created in Django Admin and assigned by the coach through the website.

Each achievement has:

- a title;
- a description;
- an icon.

Example achievements:

| Icon | Achievement |
|---|---|
| 🥋 | First Step |
| 💪 | Strong Spirit |
| 🔥 | Hard Worker |
| 🎯 | Technique of the Day |
| 😤 | Fighting Mindset |
| 🏋️ | Powerhouse |
| 🤝 | Coach's Helper |
| 🌟 | Group Role Model |
| 🎟️ | First Tournament |
| 🥇 | Tournament Champion |
| 👑 | Student of the Month |

---

## User Roles

### Coach

The coach manages groups, students, points, achievements, and student passwords.

### Student

The student only has access to their personal account and their own group rating.

The project includes role-based page protection: students cannot access coach-only sections.

---

## Tech Stack

- **Python 3.12**
- **Django 6**
- **SQLite**
- **Gunicorn**
- **Nginx**
- **HTML**
- **CSS**
- **Git**
- **Yandex Cloud**
- **Certbot / Let's Encrypt**

---

## Project Structure

```text
judo-skill/
├── accounts/
│   ├── urls.py
│   └── views.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── dojo/
│   ├── admin.py
│   ├── decorators.py
│   ├── forms.py
│   ├── models.py
│   ├── services.py
│   ├── urls.py
│   └── views.py
├── static/
│   └── css/
│       └── style.css
├── templates/
│   └── base.html
├── manage.py
├── requirements.txt
└── README.md
```

---

## Main Models

### Profile

Stores the user's role:

- coach;
- student.

### Group

A group of students that belongs to a specific coach.

### Student

Student profile:

- user account;
- group;
- first name;
- last name;
- age;
- belt;
- total points;
- emoji avatar.

### PointEvent

A point history record:

- student;
- coach;
- point amount;
- comment;
- award date.

### Achievement

Achievement directory:

- title;
- description;
- icon.

### StudentAchievement

The relation between a student and an assigned achievement.

---

## Main Pages

### Common Pages

| URL | Purpose |
|---|---|
| `/` | Home page |
| `/login/` | Sign in |
| `/logout/` | Sign out |
| `/admin/` | Django Admin |

### Coach Pages

| URL | Purpose |
|---|---|
| `/coach/` | Coach dashboard |
| `/coach/groups/create/` | Create a group |
| `/coach/groups/<id>/` | Group page |
| `/coach/groups/<id>/edit/` | Edit a group |
| `/coach/groups/<id>/delete/` | Delete a group |
| `/coach/groups/<id>/students/create/` | Add a student |
| `/coach/students/<id>/` | Student profile |
| `/coach/students/<id>/edit/` | Edit a student |
| `/coach/students/<id>/password/` | Change a student's password |
| `/coach/students/<id>/delete/` | Delete a student |
| `/coach/students/<id>/points/add/` | Award points |
| `/coach/points/<id>/edit/` | Edit a point event |
| `/coach/points/<id>/delete/` | Delete a point event |
| `/coach/students/<id>/achievements/add/` | Assign an achievement |
| `/coach/student-achievements/<id>/delete/` | Remove a student's achievement |

### Student Pages

| URL | Purpose |
|---|---|
| `/student/me/` | Student account |
| `/student/avatar/` | Change emoji avatar |

---

## Local Setup

Clone the repository:

```bash
git clone https://github.com/AHEKDOT12/judo-skill.git
cd judo-skill
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment.

Windows Git Bash:

```bash
source venv/Scripts/activate
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Apply migrations:

```bash
python manage.py migrate
```

Create a superuser:

```bash
python manage.py createsuperuser
```

Run the development server:

```bash
python manage.py runserver
```

Open the app in a browser:

```text
http://127.0.0.1:8000/
```

---

## Initial Setup

After creating a superuser, open Django Admin:

```text
http://127.0.0.1:8000/admin/
```

Then:

1. create a coach user;
2. create a `Profile` for that user with the `Coach` role;
3. create the initial achievements.

After that, the coach can use the regular website interface.

---

## Deployment

The project is deployed on a Yandex Cloud virtual machine.

Runtime flow:

```text
Internet
↓
Nginx
↓
Gunicorn
↓
Django
↓
SQLite
```

Gunicorn runs as a `systemd` service:

```bash
sudo systemctl status judo-skill
```

Nginx works as a reverse proxy and serves static files.

---

## Updating the Project on the Server

Locally:

```bash
git add .
git commit -m "Update project"
git push
```

On the server:

```bash
ssh user@server_ip
cd /home/user/judo-skill
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart judo-skill
sudo systemctl restart nginx
```

---

## Backups

The project currently uses SQLite. The database is stored in a single file:

```text
db.sqlite3
```

Daily automatic backups are configured on the server through `cron`.

Example backup script:

```bash
#!/bin/bash

BACKUP_DIR="/home/user/backups"
DB_PATH="/home/user/judo-skill/db.sqlite3"

mkdir -p "$BACKUP_DIR"

cp "$DB_PATH" "$BACKUP_DIR/db-$(date +%F-%H-%M).sqlite3"

find "$BACKUP_DIR" -name "db-*.sqlite3" -type f -mtime +14 -delete
```

Cron job:

```bash
0 3 * * * /home/user/backup_judo_db.sh
```

It creates a database copy every day at 03:00 and removes backups older than 14 days.

---

## Implemented

- user authentication;
- coach and student roles;
- role-based page protection;
- group creation, editing, and deletion;
- student creation, editing, and deletion;
- coach-side student password changes;
- point awards;
- point event editing;
- point event deletion;
- automatic point recalculation;
- rank system;
- group rating;
- student sorting by points and name;
- achievements;
- removal of assigned achievements;
- student account page;
- emoji avatar selection;
- mobile interface;
- server deployment;
- HTTPS;
- daily database backups.

---

## Possible Improvements

- connect PostgreSQL;
- add a full point history page;
- add a "Show more" button for history;
- add point history filtering by date;
- add rating export to Excel;
- add student notifications;
- add support for multiple coaches;
- add parent access;
- add attendance statistics;
- add photo uploads with automatic compression;
- add PWA mode for installing the site on a phone.

---

## Project Status

The project is a working MVP.

The core functionality is complete and is already used by a coach in a real sports club.

