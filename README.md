# Django Skeleton

**Note:** For further customization of authentication visit [Django docs](https://docs.djangoproject.com/en/4.0/topics/auth/customizing/)

---
**What does this skeleton include?**
- Custom authentication with username/email login capablities
- `.env` file with variables set for sendgrid, stripe and more...
- Necessary files for Heroku (e.g. `runtime.txt`, `Procfile`, `Pipfile.lock`, etc.)
- Postman collection for auth2 app

---
**Clone Repository**
```
git clone https://github.com/shaun-ps-04/django_rest_template.git .
git remote remove origin
rm -rf .git
git init
git branch -M main
```

Remember to uncomment `config/.env` in `.gitignore`

```bash
mkdir .venv
pipenv shell
pipenv install
py generate_sk.py  # Swap key in .env with key generated from this command
```

```bash
git add .
git commit -m "Initial Commit"
git remote add origin <path>
git push -u origin main
```

```bash
python manage.py migrate
python manage.py createsuperuser --username admin --email admin@gmail.com
```

---
(Optional) **Include e-mails and payments**
```
pipenv install sendgrid stripe
```

---
Runserver shortcut (runs on port 9000):
```
./server.sh
```