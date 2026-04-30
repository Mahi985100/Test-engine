# CGAAT Django Sample Test Engine

Features:
- User Register/Login/Logout
- Start Test Button
- Timer Countdown
- Next / Previous Question
- Auto-save answer on Next/Previous/Submit
- Submit Test
- Instant Result Generation
- Progress Bar
- Mobile Responsive UI
- Section-wise questions: Aptitude, Personality, Career Interest, Emotional Intelligence
- Dashboard and printable PDF report

## Run Steps

```bash
cd cgaat_full_django
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

Create admin:

```bash
python manage.py createsuperuser
```

Admin panel:

```text
http://127.0.0.1:8000/admin/
```

Important: sample sections and questions are automatically inserted when you run `python manage.py migrate`.
