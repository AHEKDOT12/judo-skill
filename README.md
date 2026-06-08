# 🥋 Judo Skill

**Judo Skill** — веб-приложение на Django для тренера по дзюдо, которое помогает вести прогресс учеников в игровом формате: очки, ранги, пояса, достижения, emoji-аватары, рейтинг группы и личные кабинеты учеников.

Проект сделан как реальный MVP для спортивной секции. Тренер управляет группами и учениками через сайт, а ученики заходят в личный кабинет и отслеживают свой прогресс.

---

## 🌐 Live Demo

🔗 **Demo:** https://judoskill.dpdns.org/

---

## 📌 Project Idea

В обычной спортивной секции прогресс учеников часто хранится в голове тренера, бумажных списках или таблицах.

**Judo Skill** превращает этот процесс в понятную игровую систему:

- тренер начисляет очки за тренировки, технику, дисциплину, соревнования и прогресс;
- ученик видит свой ранг, место в группе, пояс, достижения и историю начислений;
- рейтинг мотивирует учеников заниматься стабильнее;
- достижения делают процесс похожим на игру;
- emoji-аватары добавляют индивидуальность без загрузки фотографий.

---

## ✨ Features

### 👨‍🏫 Coach

Тренер может:

- создавать, редактировать и удалять группы;
- добавлять учеников в группы;
- редактировать данные учеников;
- удалять учеников;
- менять пароль ученику;
- начислять очки;
- редактировать и удалять начисления;
- выдавать достижения;
- удалять выданные достижения;
- смотреть рейтинг учеников внутри группы;
- сортировать учеников по очкам или по имени;
- видеть профиль каждого ученика.

### 🧒 Student

Ученик может:

- входить в личный кабинет;
- видеть текущий ранг;
- видеть количество очков;
- видеть прогресс до следующего ранга;
- видеть свой пояс;
- видеть своё место в группе;
- видеть рейтинг своей группы;
- видеть последние начисления очков;
- видеть полученные достижения;
- менять emoji-аватар.

---

## 🏆 Rank System

Ранг считается автоматически на основе общего количества очков ученика.

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

## 🎯 Points System

Система очков рассчитана так, чтобы обычные тренировки давали стабильный небольшой прогресс, а соревнования, аттестации и серьёзные достижения давали заметный прирост.

| Action | Points |
|---|---:|
| Attended training | +5 |
| Worked well during training | +10 |
| Learned a basic technique | +15 |
| Performed a technique well | +20 |
| Used a technique in sparring | +35 |
| Competition participation | +50 |
| 3rd place in competition | +120 |
| 2nd place in competition | +160 |
| 1st place in competition | +220 |
| Passed belt exam | +150 |
| New belt | +200 |
| Student of the month | +200 |

---

## 🎖️ Achievements

Achievements are created through Django Admin and awarded by the coach through the website.

Each achievement has:

- title;
- description;
- icon.

Examples:

| Icon | Achievement |
|---|---|
| 🥋 | First Step |
| 💪 | Strong Spirit |
| 🔥 | Hard Worker |
| 🎯 | Technique of the Day |
| 😤 | Fighting Mood |
| 🏋️ | Strongman |
| 🤝 | Coach Assistant |
| 🌟 | Example for the Group |
| 🎟️ | First Tournament |
| 🥇 | Tournament Champion |
| 👑 | Student of the Month |

---

## 👥 User Roles

### Coach

The coach manages groups, students, points, achievements and passwords.

### Student

The student only has access to their own profile and group rating.

Role-based access protection is implemented: students cannot access coach pages.

---

## 🛠️ Tech Stack

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

## 📁 Project Structure

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
│   ├── base.html
│   └── includes/
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🧩 Main Models

### Profile

Stores the user role:

- coach;
- student.

### Group

A student group owned by a specific coach.

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

Point history record:

- student;
- coach;
- points;
- comment;
- created date.

### Achievement

Achievement reference model:

- title;
- description;
- icon.

### StudentAchievement

Connection between student and awarded achievement.

---

## 🔗 Main URLs

### Common

| URL | Description |
|---|---|
| `/` | Home page |
| `/login/` | Login |
| `/logout/` | Logout |
| `/admin/` | Django Admin |

### Coach

| URL | Description |
|---|---|
| `/coach/` | Coach dashboard |
| `/coach/groups/create/` | Create group |
| `/coach/groups/<id>/` | Group detail |
| `/coach/groups/<id>/edit/` | Edit group |
| `/coach/groups/<id>/delete/` | Delete group |
| `/coach/groups/<id>/students/create/` | Add student |
| `/coach/students/<id>/` | Student profile |
| `/coach/students/<id>/edit/` | Edit student |
| `/coach/students/<id>/password/` | Change student password |
| `/coach/students/<id>/delete/` | Delete student |
| `/coach/students/<id>/points/add/` | Add points |
| `/coach/points/<id>/edit/` | Edit point event |
| `/coach/points/<id>/delete/` | Delete point event |
| `/coach/students/<id>/achievements/add/` | Award achievement |

### Student

| URL | Description |
|---|---|
| `/student/me/` | Student dashboard |
| `/student/avatar/` | Change emoji avatar |

---

## 🚀 Local Installation

Clone the repository:

```bash
git clone https://github.com/USERNAME/judo-skill.git
cd judo-skill
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it.

For Windows Git Bash:

```bash
source venv/Scripts/activate
```

For Linux/macOS:

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

Open in browser:

```text
http://127.0.0.1:8000/
```

---

## ⚙️ First Setup

After creating a superuser, open Django Admin:

```text
http://127.0.0.1:8000/admin/
```

Then:

1. create a coach user;
2. create a `Profile` with role `Coach`;
3. create basic achievements.

After that, the coach can use the regular website interface.

---

## 🖥️ Deployment

The project is deployed on a Yandex Cloud virtual machine.

Production scheme:

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

## 🔄 Updating the Project on Server

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

## 💾 Backups

The project currently uses SQLite. The database is stored in one file:

```text
db.sqlite3
```

Daily automatic backups are configured through `cron`.

Backup script example:

```bash
#!/bin/bash

BACKUP_DIR="/home/user/backups"
DB_PATH="/home/user/judo-skill/db.sqlite3"

mkdir -p "$BACKUP_DIR"

cp "$DB_PATH" "$BACKUP_DIR/db-$(date +%F-%H-%M).sqlite3"

find "$BACKUP_DIR" -name "db-*.sqlite3" -type f -mtime +14 -delete
```

Cron task:

```bash
0 3 * * * /home/user/backup_judo_db.sh
```

This creates a database backup every day at 03:00 and removes backups older than 14 days.

---

## ✅ Implemented

- user authentication;
- coach and student roles;
- role-based page protection;
- group CRUD;
- student CRUD;
- password change for students by coach;
- point assignment;
- point editing;
- point deletion;
- automatic point recalculation;
- rank system;
- group rating;
- sorting students by points and name;
- achievements;
- deleting awarded achievements;
- student dashboard;
- emoji avatar selection;
- mobile-first UI;
- production deployment;
- HTTPS;
- daily database backups.

---

## 📈 Future Improvements

- PostgreSQL support;
- full point history page;
- “Show more” button for history;
- filtering point events by date;
- rating export to Excel;
- student notifications;
- multiple coaches;
- parent access;
- attendance statistics;
- compressed photo avatars;
- PWA mode for installing the website on a phone.

---

## 📍 Project Status

The project is a working MVP.

The core functionality is ready and can be used by a coach in a real sports section.
